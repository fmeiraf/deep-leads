import asyncio
import os
import random
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Dict, List

import pyalex
from pydantic import BaseModel, Field
from rich import print as rprint
from rich.console import Console
from tqdm import tqdm

from src.agents.utils.build_final_query import build_final_query
from src.types import (
    Lead,
    LeadResults,
    OpenAlexResults,
    QueryType,
    ResearchParams,
    Sample,
)

COUNTRIES = {
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "BR": "Brazil",
}


ROLES = [
    "researchers",
    "experts",
    "scientists",
    "professors",
    "specialists",
]

START_YEAR = 2023
MAX_RESULTS_PER_PAGE = 200

# Rate limiting semaphore - allow up to 10 concurrent requests
API_SEMAPHORE = asyncio.Semaphore(10)
API_DELAY = 0.1  # 100ms delay between requests to ensure ~10 requests/second


async def rate_limited_api_call(api_call_func):
    """Rate-limited wrapper for OpenAlex API calls"""
    async with API_SEMAPHORE:
        try:
            result = api_call_func()
            await asyncio.sleep(API_DELAY)
            return result
        except Exception as e:
            await asyncio.sleep(API_DELAY)  # Still delay on errors
            raise e


class GenerationConfig(BaseModel):
    """Configuration for synthetic query generation"""

    target_queries: int = Field(
        default=1000, description="Target number of queries to generate"
    )
    batch_size: int = Field(
        default=250, description="Number of queries to process in each batch"
    )
    max_results_per_query: int = Field(
        default=25, description="Maximum results to fetch per query"
    )
    checkpoint_dir: str = Field(
        default="checkpoints", description="Directory to save checkpoints"
    )
    output_file: str = Field(
        default="synthetic_queries.json", description="Final output file"
    )
    country_based_queries_ratio: float = Field(
        default=0.1, description="Ratio of country-based queries"
    )
    city_based_queries_ratio: float = Field(
        default=0.4, description="Ratio of city-based queries"
    )
    institution_based_queries_ratio: float = Field(
        default=0.5, description="Ratio of institution-based queries"
    )


class SyntheticQueryGenerator:
    """Generates synthetic academic queries using OpenAlex data"""

    def __init__(self, config: GenerationConfig):
        self.config = config
        self.console = Console()
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.final_results = []
        self.country_string = "|".join(COUNTRIES.keys())
        self.start_year = START_YEAR

        # Initialize PyAlex
        pyalex.config.email = os.getenv("PYALEX_EMAIL")
        self.city_search_cache = {}

        # Initialize the body of work
        self.institution_based_searches = []
        self.city_based_searches = []
        self.country_based_searches = []
        self.field_based_searches = []

        # getting the number of queries to generate for each type
        self.institution_based_queries_target = int(
            self.config.target_queries * self.config.institution_based_queries_ratio
        )
        self.city_based_queries_target = int(
            self.config.target_queries * self.config.city_based_queries_ratio
        )
        self.country_based_queries_target = int(
            self.config.target_queries * self.config.country_based_queries_ratio
        )
        self.role_variations = [
            "researchers",
            "experts",
            "scientists",
            "professors",
            "specialists",
            "academics",
            "researchers",
        ]

    async def gather_data(self) -> None:
        """Initialize OpenAlex data caches"""
        rprint("[white]Initializing main OpenAlex query and topic maps...[/white]")

        await self._get_main_query()
        await self._get_topic_maps()

        rprint("[green]Starting building all the queries...[/green]")

        await self._get_city_based_searches()
        await self._get_country_based_searches()
        await self._get_institution_based_searches()

        rprint(
            f"[green]Cached {len(self.institution_based_searches)} institution-based searches,"
            f"{len(self.city_based_searches)} city-based searches,"
            f"{len(self.country_based_searches)} country-based searches[/green]"
        )

    async def _execute_openalex_query(
        self, topic: Dict, location_or_institution: Dict, is_institution: bool
    ) -> List[Lead]:
        """Execute OpenAlex query and convert results to Lead objects with rate limiting"""
        try:
            # Search for works using topics.id filter with rate limiting
            # Try with publication date filter first, fallback without it if needed
            try:
                if is_institution:
                    works = await rate_limited_api_call(
                        lambda: pyalex.Works()
                        .filter(**{"topics.id": topic["id"]})
                        .filter(
                            **{
                                "authorships.institutions.id": location_or_institution[
                                    "id"
                                ]
                            }
                        )
                        .filter(**{"publication_date": ">2024-06-01"})
                        .get(per_page=self.config.max_results_per_query)
                    )
                else:
                    works = await rate_limited_api_call(
                        lambda: pyalex.Works()
                        .filter(**{"topics.id": topic["id"]})
                        .filter(
                            **{
                                "authorships.institutions.country_code": location_or_institution[
                                    "country_code"
                                ]
                            }
                        )
                        .filter(**{"publication_date": ">2024-06-01"})
                        .get(per_page=self.config.max_results_per_query)
                    )
            except Exception as date_filter_error:
                # If date filtering fails, try without it
                rprint(
                    f"[yellow]Date filter failed, trying without date restriction: {date_filter_error}[/yellow]"
                )

                if is_institution:
                    works = await rate_limited_api_call(
                        lambda: pyalex.Works()
                        .filter(**{"topics.id": topic["id"]})
                        .filter(
                            **{
                                "authorships.institutions.id": location_or_institution[
                                    "id"
                                ]
                            }
                        )
                        .get(per_page=self.config.max_results_per_query)
                    )
                else:
                    works = await rate_limited_api_call(
                        lambda: pyalex.Works()
                        .filter(**{"topics.id": topic["id"]})
                        .filter(
                            **{
                                "authorships.institutions.country_code": location_or_institution[
                                    "country_code"
                                ]
                            }
                        )
                        .get(per_page=self.config.max_results_per_query)
                    )

            # Extract unique authors
            authors_seen = set()
            leads = []

            for work in works:
                for authorship in work.get("authorships", []):
                    author = authorship.get("author", {})
                    author_id = author.get("id")

                    if author_id and author_id not in authors_seen:
                        authors_seen.add(author_id)

                        # Get author institutions as list
                        institutions = []
                        for inst in authorship.get("institutions", []):
                            if inst.get("display_name"):
                                institutions.append(inst["display_name"])

                        # If no institutions found, add placeholder
                        if not institutions:
                            institutions = ["Unknown Institution"]

                        # Department as list - use topic field
                        departments = [topic["display_name"]]

                        lead = Lead(
                            name=author.get("display_name", "Unknown"),
                            title="Researcher",
                            headline=f"Researcher at {institutions[0]}",
                            location=institutions[0],
                            summary=f"Author in {topic['display_name']} field",
                            institution=institutions,  # List of institutions
                            department=departments,  # List of departments
                        )
                        leads.append(lead)

                        if len(leads) >= self.config.max_results_per_query:
                            break

                    if len(leads) >= self.config.max_results_per_query:
                        break

            return leads

        except Exception as e:
            rprint(f"[red]Error executing OpenAlex query: {e}[/red]")
            return []

    async def _execute_location_based_query(
        self, topic: Dict, city_data: Dict
    ) -> List[Lead]:
        pass

    def get_current_combination_counts(self):
        institution_combinations = sum(
            len(topics) for topics in self.topics_per_institution.values()
        )
        city_combinations = sum(len(topics) for topics in self.topics_per_city.values())
        country_combinations = sum(
            len(topics) for topics in self.topics_per_country.values()
        )
        total_combinations = (
            institution_combinations + city_combinations + country_combinations
        )
        return (
            total_combinations,
            institution_combinations,
            city_combinations,
            country_combinations,
        )

    async def _get_main_query(self):
        """This is main query to iterate over and generate all the necessary queries"""

        self.main_query = (
            pyalex.Works()
            .filter(publication_year=f">{self.start_year}")
            .filter(authorships={"institutions.country_code": self.country_string})
        )

    async def _get_topic_maps(self):
        """Creates a map of topic ids for countries, cities and institutions"""
        self.topics_per_country = defaultdict(set)  # {country_code: [topic_id_1, ..]}
        self.topics_per_city = defaultdict(set)  # {city: [topic_id_1, ..]}
        self.topics_per_institution = defaultdict(
            set
        )  # {institution_id: [topic_id_1, ..]}

        for record in chain(*self.main_query.paginate(per_page=200)):
            # checking if we have enough combinations
            (
                total_combinations,
                valid_institution_queries,
                valid_city_queries,
                valid_country_queries,
            ) = self.get_current_combination_counts()
            if total_combinations >= self.config.target_queries:
                return

            # starting to process the record

            authorships = record.get("authorships", [])
            if not authorships:
                continue

            primary_topic = record.get("primary_topic", {})
            if not primary_topic:
                continue

            for author in authorships:
                institution = author.get("institutions", [])
                if not institution:
                    continue
                for inst in institution:
                    # refreshing the counts
                    (
                        total_combinations,
                        valid_institution_queries,
                        valid_city_queries,
                        valid_country_queries,
                    ) = self.get_current_combination_counts()

                    if inst.get("country_code") in COUNTRIES.keys():
                        # Adding record on country level
                        if valid_country_queries < self.country_based_queries_target:
                            self.topics_per_country[inst.get("country_code")].add(
                                primary_topic["id"]
                            )

                        # Adding record on institution level
                        if (
                            valid_institution_queries
                            < self.institution_based_queries_target
                        ):
                            self.topics_per_institution[inst.get("id")].add(
                                primary_topic["id"]
                            )

                        # Adding record on city level

                        institution_search = (
                            pyalex.Institutions()
                            .search_filter(display_name=inst.get("display_name"))
                            .get()
                        )

                        for inst_ in institution_search:
                            if valid_city_queries < self.city_based_queries_target:
                                if inst_.get("id") == inst.get("id"):
                                    city = inst_.get("geo", {}).get("city")
                                    if city:
                                        self.topics_per_city[city].add(
                                            (
                                                primary_topic["id"],
                                                inst.get("country_code"),
                                            )
                                        )

    async def _get_city_based_searches(self) -> List[Dict]:
        rprint("[cyan]Processing city-based searches...[/cyan]")
        for city in tqdm(self.topics_per_city.keys(), desc="City-based searches"):
            for topic_id, country_code in self.topics_per_city[city]:
                self.city_based_searches.append(
                    await self._process_city_based_searches(
                        topic_id, country_code, city
                    )
                )

    async def _get_country_based_searches(self) -> List[Dict]:
        rprint("[cyan]Processing country-based searches...[/cyan]")
        for country_code in tqdm(
            self.topics_per_country.keys(), desc="Country-based searches"
        ):
            for topic_id in self.topics_per_country[country_code]:
                self.country_based_searches.append(
                    await self._process_country_based_searches(topic_id, country_code)
                )

    async def _get_institution_based_searches(self) -> List[Dict]:
        """Given a topic and an institution, generate a list of leads for each topic"""
        rprint("[cyan]Processing institution-based searches...[/cyan]")
        for institution_id in tqdm(
            self.topics_per_institution.keys(), desc="Institution-based searches"
        ):
            for topic_id in self.topics_per_institution[institution_id]:
                self.institution_based_searches.append(
                    await self._process_institution_based_searches(
                        topic_id, institution_id
                    )
                )

    async def _process_city_based_searches(
        self, topic_id: str, country_code: str, city: str
    ) -> Sample:
        """Process institution-based searches for a list of topics and an institution"""
        query_results = (
            pyalex.Works()
            .filter(publication_year=f">{self.start_year}")
            .filter(authorships={"institutions.country_code": country_code})
            .filter(topics={"id": topic_id})
            .get()
        )

        leads = []
        title = random.choice(ROLES)
        topic_name = ""
        institution_name = ""
        openalex_results = None
        selected_authors = set()

        for record in query_results:
            if record.get("authorships", []):
                for authorship in record.get("authorships", []):
                    if authorship.get("institutions", []):
                        for inst in authorship.get("institutions", []):
                            if inst.get("country_code") == country_code:
                                if inst.get("id") in self.city_search_cache:
                                    city_search = self.city_search_cache[inst.get("id")]
                                else:
                                    institution_code = inst.get("id").split("/")[-1]
                                    institution_search = pyalex.Institutions()[
                                        institution_code
                                    ]

                                    city_search = institution_search.get("geo", {}).get(
                                        "city"
                                    )
                                    self.city_search_cache[inst.get("id")] = city_search

                                if city_search != city:
                                    continue

                                # getting relevant openalex data
                                topic = record.get("primary_topic", {})
                                topic_name = topic.get("display_name")
                                topic_keywords = topic.get("keywords")
                                topic_domain = topic.get("domain").get("display_name")
                                topic_field = topic.get("field").get("display_name")
                                topic_subfield = topic.get("subfield").get(
                                    "display_name"
                                )
                                institution_name = inst.get("display_name")
                                target_researcher_id = authorship.get("author", {}).get(
                                    "id"
                                )
                                target_researcher_name = authorship.get(
                                    "author", {}
                                ).get("display_name")
                                work_id = record.get("id")

                                if target_researcher_id in selected_authors:
                                    continue

                                selected_authors.add(target_researcher_id)

                                # getting the final leads
                                leads.append(
                                    Lead(
                                        name=target_researcher_name,
                                        title=title,
                                        headline=f"Researcher in {institution_name}",
                                        institution=institution_name,
                                        source_url=target_researcher_id,
                                    )
                                )

                                openalex_results = OpenAlexResults(
                                    topic_id=topic_id,
                                    topic_display_name=topic_name,
                                    topic_keywords=topic_keywords,
                                    topic_domain=topic_domain,
                                    topic_field=topic_field,
                                    topic_subfield=topic_subfield,
                                    institution_id=inst.get("id"),
                                    institution_country=country_code,
                                    city=city,
                                    target_researcher_id=target_researcher_id,
                                    target_researcher_name=target_researcher_name,
                                    work_id=work_id,
                                )

        # Validate that we have all required data
        if not openalex_results or not topic_name or not leads:
            raise ValueError(
                f"Missing required data for city {city}, country {country_code}, topic {topic_id}: "
                f"openalex_results={openalex_results is not None}, "
                f"topic_name='{topic_name}', "
                f"leads_count={len(leads)}"
            )

        research_params = ResearchParams(
            who_query=title,
            what_query=topic_name,
            where_query=city,
        )

        query_string = build_final_query(research_params)

        sample = Sample(
            query_params=research_params,
            query_string=query_string,
            query_type=QueryType.INSTITUTION_FOCUSED,
            expected_results=LeadResults(leads=leads),
            openalex_results=openalex_results,
        )

        return sample

    async def _process_country_based_searches(
        self, topic_id: str, country_code: str
    ) -> Sample:
        """Process institution-based searches for a list of topics and an institution"""
        query_results = (
            pyalex.Works()
            .filter(publication_year=f">{self.start_year}")
            .filter(authorships={"institutions.country_code": country_code})
            .filter(topics={"id": topic_id})
            .get()
        )

        leads = []
        title = random.choice(ROLES)
        topic_name = ""
        institution_name = ""
        openalex_results = None
        selected_authors = set()

        for record in query_results:
            if record.get("authorships", []):
                for authorship in record.get("authorships", []):
                    if authorship.get("institutions", []):
                        for inst in authorship.get("institutions", []):
                            if inst.get("country_code") == country_code:
                                # getting relevant openalex data
                                topic = record.get("primary_topic", {})
                                topic_name = topic.get("display_name")
                                topic_keywords = topic.get("keywords")
                                topic_domain = topic.get("domain").get("display_name")
                                topic_field = topic.get("field").get("display_name")
                                topic_subfield = topic.get("subfield").get(
                                    "display_name"
                                )
                                institution_name = inst.get("display_name")
                                target_researcher_id = authorship.get("author", {}).get(
                                    "id"
                                )
                                target_researcher_name = authorship.get(
                                    "author", {}
                                ).get("display_name")
                                work_id = record.get("id")

                                if target_researcher_id in selected_authors:
                                    continue

                                selected_authors.add(target_researcher_id)

                                # getting the final leads
                                leads.append(
                                    Lead(
                                        name=target_researcher_name,
                                        title=title,
                                        headline=f"Researcher in {institution_name}",
                                        institution=institution_name,
                                        source_url=target_researcher_id,
                                    )
                                )

                                openalex_results = OpenAlexResults(
                                    topic_id=topic_id,
                                    topic_display_name=topic_name,
                                    topic_keywords=topic_keywords,
                                    topic_domain=topic_domain,
                                    topic_field=topic_field,
                                    topic_subfield=topic_subfield,
                                    institution_id=inst.get("id"),
                                    institution_country=country_code,
                                    target_researcher_id=target_researcher_id,
                                    target_researcher_name=target_researcher_name,
                                    work_id=work_id,
                                )

        # Validate that we have all required data
        if not openalex_results or not topic_name or not leads:
            raise ValueError(
                f"Missing required data for country {country_code}, topic {topic_id}: "
                f"openalex_results={openalex_results is not None}, "
                f"topic_name='{topic_name}', "
                f"leads_count={len(leads)}"
            )

        research_params = ResearchParams(
            who_query=title,
            what_query=topic_name,
            where_query=COUNTRIES[country_code],
        )
        query_string = build_final_query(research_params)

        sample = Sample(
            query_params=research_params,
            query_string=query_string,
            query_type=QueryType.INSTITUTION_FOCUSED,
            expected_results=LeadResults(leads=leads),
            openalex_results=openalex_results,
        )

        return sample

    async def _process_institution_based_searches(
        self, topic_id: str, institution_id: str
    ) -> Sample:
        """Process institution-based searches for a list of topics and an institution"""
        query_results = (
            pyalex.Works()
            .filter(publication_year=f">{self.start_year}")
            .filter(authorships={"institutions.country_code": self.country_string})
            .filter(authorships={"institutions.id": institution_id})
            .filter(topics={"id": topic_id})
            .get()
        )

        leads = []
        title = random.choice(ROLES)
        topic_name = ""
        institution_name = ""
        openalex_results = None
        selected_authors = set()

        for record in query_results:
            if record.get("authorships", []):
                for authorship in record.get("authorships", []):
                    if authorship.get("institutions", []):
                        for inst in authorship.get("institutions", []):
                            if inst.get("id") == institution_id:
                                # getting relevant openalex data
                                topic = record.get("primary_topic", {})
                                topic_name = topic.get("display_name")
                                topic_keywords = topic.get("keywords")
                                topic_domain = topic.get("domain").get("display_name")
                                topic_field = topic.get("field").get("display_name")
                                topic_subfield = topic.get("subfield").get(
                                    "display_name"
                                )
                                institution_name = inst.get("display_name")
                                target_researcher_id = authorship.get("author", {}).get(
                                    "id"
                                )
                                target_researcher_name = authorship.get(
                                    "author", {}
                                ).get("display_name")
                                work_id = record.get("id")

                                if target_researcher_id in selected_authors:
                                    continue

                                selected_authors.add(target_researcher_id)

                                # getting the final leads
                                leads.append(
                                    Lead(
                                        name=target_researcher_name,
                                        title=title,
                                        headline=f"Researcher in {inst.get('display_name')}",
                                        institution=inst.get("display_name"),
                                        source_url=target_researcher_id,
                                    )
                                )

                                openalex_results = OpenAlexResults(
                                    topic_id=topic_id,
                                    topic_display_name=topic_name,
                                    topic_keywords=topic_keywords,
                                    topic_domain=topic_domain,
                                    topic_field=topic_field,
                                    topic_subfield=topic_subfield,
                                    institution_id=institution_id,
                                    institution_country=inst.get("country_code"),
                                    target_researcher_id=target_researcher_id,
                                    target_researcher_name=target_researcher_name,
                                    work_id=work_id,
                                )

        # Validate that we have all required data
        if not openalex_results or not topic_name or not leads:
            raise ValueError(
                f"Missing required data for institution {institution_id}, topic {topic_id}: "
                f"openalex_results={openalex_results is not None}, "
                f"topic_name='{topic_name}', "
                f"leads_count={len(leads)}"
            )

        research_params = ResearchParams(
            who_query=title,
            what_query=topic_name,
            where_query=institution_name,
        )
        query_string = build_final_query(research_params)

        sample = Sample(
            query_params=research_params,
            query_string=query_string,
            query_type=QueryType.INSTITUTION_FOCUSED,
            expected_results=LeadResults(leads=leads),
            openalex_results=openalex_results,
        )

        return sample


async def main():
    """Example usage of the synthetic query generator"""
    config = GenerationConfig(
        target_queries=100,  # Start with smaller number for testing
        batch_size=10,
        max_results_per_query=5,
        checkpoint_dir="notebooks/checkpoints/synthetic_queries",
        output_file="notebooks/synthetic_queries_sample.json",
    )

    generator = SyntheticQueryGenerator(config)
    results = await generator.generate_queries()

    print(f"\nGenerated {len(results)} synthetic queries!")

    # Show a few examples
    print("\nSample queries:")
    for i, result in enumerate(results[:3]):
        print(f"\n{i + 1}. {result.query_string}")
        print(f"   Found {len(result.results.leads)} leads")
        if result.results.leads:
            print(f"   Sample lead: {result.results.leads[0].name}")


if __name__ == "__main__":
    asyncio.run(main())

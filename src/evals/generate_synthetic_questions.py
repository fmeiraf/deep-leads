import asyncio
import json
import os
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
    parallel_batch_size: int = Field(default=3)


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

        # Checkpoint files
        self.gathered_data_file = self.checkpoint_dir / "gathered_data.json"
        self.checkpoint_pattern = "checkpoint_batch_{}.json"
        self.progress_file = self.checkpoint_dir / "progress.json"

    def save_gathered_data(self) -> None:
        """Save the gathered data structures to JSON for recovery"""
        gathered_data = {
            "topics_per_country": {
                k: list(v) for k, v in self.topics_per_country.items()
            },
            "topics_per_city": {k: list(v) for k, v in self.topics_per_city.items()},
            "topics_per_institution": {
                k: list(v) for k, v in self.topics_per_institution.items()
            },
            "city_search_cache": self.city_search_cache,
        }

        with open(self.gathered_data_file, "w") as f:
            json.dump(gathered_data, f, indent=2)

        rprint(f"[green]Saved gathered data to {self.gathered_data_file}[/green]")

    def load_gathered_data(self) -> bool:
        """Load gathered data from JSON checkpoint"""
        if not self.gathered_data_file.exists():
            return False

        try:
            with open(self.gathered_data_file, "r") as f:
                gathered_data = json.load(f)

            # Convert back to defaultdict with sets
            self.topics_per_country = defaultdict(set)
            for k, v in gathered_data["topics_per_country"].items():
                self.topics_per_country[k] = set(v)

            self.topics_per_city = defaultdict(set)
            for k, v in gathered_data["topics_per_city"].items():
                self.topics_per_city[k] = set(
                    tuple(item) if isinstance(item, list) else item for item in v
                )

            self.topics_per_institution = defaultdict(set)
            for k, v in gathered_data["topics_per_institution"].items():
                self.topics_per_institution[k] = set(v)

            self.city_search_cache = gathered_data.get("city_search_cache", {})

            rprint(
                f"[green]Loaded gathered data from {self.gathered_data_file}[/green]"
            )
            return True

        except Exception as e:
            rprint(f"[red]Error loading gathered data: {e}[/red]")
            return False

    def has_gathered_data_checkpoint(self) -> bool:
        """Check if gathered data checkpoint exists"""
        return self.gathered_data_file.exists()

    def save_checkpoint(self, batch_num: int, results: List[Sample]) -> None:
        """Save checkpoint for a batch of results"""
        checkpoint_file = self.checkpoint_dir / self.checkpoint_pattern.format(
            batch_num
        )

        # Convert Sample objects to dictionaries for JSON serialization
        checkpoint_data = {
            "batch_num": batch_num,
            "results": [sample.dict() for sample in results],
            "timestamp": asyncio.get_event_loop().time(),
        }

        with open(checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)

        rprint(
            f"[green]Saved checkpoint for batch {batch_num} to {checkpoint_file}[/green]"
        )

    def load_checkpoint(self, batch_num: int) -> List[Sample]:
        """Load checkpoint for a specific batch"""
        checkpoint_file = self.checkpoint_dir / self.checkpoint_pattern.format(
            batch_num
        )

        if not checkpoint_file.exists():
            return []

        try:
            with open(checkpoint_file, "r") as f:
                checkpoint_data = json.load(f)

            # Convert dictionaries back to Sample objects
            results = [
                Sample(**sample_dict) for sample_dict in checkpoint_data["results"]
            ]
            rprint(
                f"[green]Loaded checkpoint for batch {batch_num} with {len(results)} results[/green]"
            )
            return results

        except Exception as e:
            rprint(f"[red]Error loading checkpoint for batch {batch_num}: {e}[/red]")
            return []

    def get_checkpoint_files(self) -> List[int]:
        """Get list of existing checkpoint batch numbers"""
        checkpoint_files = []
        for file in self.checkpoint_dir.glob("checkpoint_batch_*.json"):
            try:
                batch_num = int(file.stem.split("_")[-1])
                checkpoint_files.append(batch_num)
            except ValueError:
                continue
        return sorted(checkpoint_files)

    def save_progress(self, completed_batches: List[int], total_results: int) -> None:
        """Save progress information"""
        progress_data = {
            "completed_batches": completed_batches,
            "total_results": total_results,
            "timestamp": asyncio.get_event_loop().time(),
        }

        with open(self.progress_file, "w") as f:
            json.dump(progress_data, f, indent=2)

    def load_progress(self) -> Dict:
        """Load progress information"""
        if not self.progress_file.exists():
            return {"completed_batches": [], "total_results": 0}

        try:
            with open(self.progress_file, "r") as f:
                return json.load(f)
        except Exception as e:
            rprint(f"[red]Error loading progress: {e}[/red]")
            return {"completed_batches": [], "total_results": 0}

    def cleanup_checkpoints(self) -> None:
        """Clean up checkpoint files after successful completion"""
        try:
            # Remove all checkpoint files
            for file in self.checkpoint_dir.glob("checkpoint_batch_*.json"):
                file.unlink()

            # Remove progress file
            if self.progress_file.exists():
                self.progress_file.unlink()

            # Keep gathered_data.json as it might be useful for future runs
            rprint("[green]Cleaned up checkpoint files[/green]")

        except Exception as e:
            rprint(
                f"[yellow]Warning: Could not clean up checkpoint files: {e}[/yellow]"
            )

    async def generate_queries(self) -> List[Sample]:
        """Generate synthetic queries with checkpointing and recovery"""
        rprint("[cyan]Starting synthetic query generation with checkpointing...[/cyan]")

        # Check for existing progress
        progress = self.load_progress()
        completed_batches = progress.get("completed_batches", [])
        all_results = []

        # Load existing checkpoints
        for batch_num in completed_batches:
            batch_results = self.load_checkpoint(batch_num)
            all_results.extend(batch_results)

        if all_results:
            rprint(
                f"[green]Recovered {len(all_results)} results from {len(completed_batches)} completed batches[/green]"
            )

        # Load or gather data (this populates the search lists with Sample objects)
        if not self.has_gathered_data_checkpoint():
            await self.gather_data()
            self.save_gathered_data()
        else:
            rprint("[cyan]Loading gathered data from checkpoint...[/cyan]")
            self.load_gathered_data()
            # Still need to build the searches from loaded data
            await self._build_searches_from_loaded_data()

        # Get all searches to process
        all_searches = (
            self.institution_based_searches
            + self.city_based_searches
            + self.country_based_searches
        )

        # Filter out already processed searches
        remaining_searches = all_searches[len(all_results) :]

        if not remaining_searches:
            rprint("[green]All queries already generated![/green]")
            return all_results

        # Process in batches
        batch_size = self.config.batch_size
        total_batches = (len(remaining_searches) + batch_size - 1) // batch_size

        rprint(
            f"[cyan]Processing {len(remaining_searches)} remaining searches in {total_batches} batches[/cyan]"
        )

        for batch_idx in range(total_batches):
            batch_num = len(completed_batches) + batch_idx
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(remaining_searches))
            batch_searches = remaining_searches[start_idx:end_idx]

            rprint(
                f"[cyan]Processing batch {batch_num + 1}/{total_batches + len(completed_batches)} ({len(batch_searches)} searches)[/cyan]"
            )

            # The searches are already Sample objects, so we can directly save them
            batch_results = batch_searches

            # Save checkpoint
            self.save_checkpoint(batch_num, batch_results)
            all_results.extend(batch_results)

            # Update progress
            completed_batches.append(batch_num)
            self.save_progress(completed_batches, len(all_results))

            rprint(
                f"[green]Completed batch {batch_num + 1}, total results: {len(all_results)}[/green]"
            )

        # Save final results
        final_output = self.checkpoint_dir.parent / self.config.output_file
        with open(final_output, "w") as f:
            json.dump([sample.dict() for sample in all_results], f, indent=2)

        rprint(
            f"[green]Generated {len(all_results)} synthetic queries and saved to {final_output}[/green]"
        )

        # Optional cleanup of checkpoints after successful completion
        # Uncomment the next line if you want to automatically clean up checkpoints
        # self.cleanup_checkpoints()

        return all_results

    async def _build_searches_from_loaded_data(self) -> None:
        """Build search lists from loaded data"""
        if not self.institution_based_searches:
            await self._get_institution_based_searches()
        if not self.city_based_searches:
            await self._get_city_based_searches()
        if not self.country_based_searches:
            await self._get_country_based_searches()

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
                        try:
                            institution_search = (
                                pyalex.Institutions()
                                .search_filter(display_name=inst.get("display_name"))
                                .get()
                            )
                        except Exception as e:
                            rprint(f"[red]Error searching for institution: {e}[/red]")
                            continue

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

        # Flatten all city-topic combinations into a single list
        all_combinations = []
        for city in self.topics_per_city.keys():
            for topic_id, country_code in self.topics_per_city[city]:
                all_combinations.append((topic_id, country_code, city))

        # Process in batches of 5
        batch_size = self.config.parallel_batch_size
        total_batches = (len(all_combinations) + batch_size - 1) // batch_size

        rprint(
            f"[cyan]Processing {len(all_combinations)} city-based searches in {total_batches} batches of {batch_size}[/cyan]"
        )

        with tqdm(total=len(all_combinations), desc="City-based searches") as pbar:
            for batch_start in range(0, len(all_combinations), batch_size):
                batch_end = min(batch_start + batch_size, len(all_combinations))
                batch_combinations = all_combinations[batch_start:batch_end]

                # Create tasks for this batch
                tasks = []
                for topic_id, country_code, city in batch_combinations:
                    tasks.append(
                        self._process_city_based_searches(topic_id, country_code, city)
                    )

                # Run batch in parallel
                batch_results = await asyncio.gather(*tasks)

                # Add results to the main list
                self.city_based_searches.extend(batch_results)

                # Update progress bar
                pbar.update(len(batch_combinations))

                # Optional: Add a small delay between batches to be respectful to APIs
                if batch_start + batch_size < len(all_combinations):
                    await asyncio.sleep(0.1)

    async def _get_country_based_searches(self) -> List[Dict]:
        rprint("[cyan]Processing country-based searches...[/cyan]")

        # Flatten all country-topic combinations into a single list
        all_combinations = []
        for country_code in self.topics_per_country.keys():
            for topic_id in self.topics_per_country[country_code]:
                all_combinations.append((topic_id, country_code))

        # Process in batches of 5
        batch_size = self.config.parallel_batch_size
        total_batches = (len(all_combinations) + batch_size - 1) // batch_size

        rprint(
            f"[cyan]Processing {len(all_combinations)} country-based searches in {total_batches} batches of {batch_size}[/cyan]"
        )

        with tqdm(total=len(all_combinations), desc="Country-based searches") as pbar:
            for batch_start in range(0, len(all_combinations), batch_size):
                batch_end = min(batch_start + batch_size, len(all_combinations))
                batch_combinations = all_combinations[batch_start:batch_end]

                # Create tasks for this batch
                tasks = []
                for topic_id, country_code in batch_combinations:
                    tasks.append(
                        self._process_country_based_searches(topic_id, country_code)
                    )

                # Run batch in parallel
                batch_results = await asyncio.gather(*tasks)

                # Add results to the main list
                self.country_based_searches.extend(batch_results)

                # Update progress bar
                pbar.update(len(batch_combinations))

                # Optional: Add a small delay between batches to be respectful to APIs
                if batch_start + batch_size < len(all_combinations):
                    await asyncio.sleep(0.1)

    async def _get_institution_based_searches(self) -> List[Dict]:
        """Given a topic and an institution, generate a list of leads for each topic"""
        rprint("[cyan]Processing institution-based searches...[/cyan]")

        # Flatten all institution-topic combinations into a single list
        all_combinations = []
        for institution_id in self.topics_per_institution.keys():
            for topic_id in self.topics_per_institution[institution_id]:
                all_combinations.append((topic_id, institution_id))

        # Process in batches of 5
        batch_size = self.config.parallel_batch_size
        total_batches = (len(all_combinations) + batch_size - 1) // batch_size

        rprint(
            f"[cyan]Processing {len(all_combinations)} institution-based searches in {total_batches} batches of {batch_size}[/cyan]"
        )

        with tqdm(
            total=len(all_combinations), desc="Institution-based searches"
        ) as pbar:
            for batch_start in range(0, len(all_combinations), batch_size):
                batch_end = min(batch_start + batch_size, len(all_combinations))
                batch_combinations = all_combinations[batch_start:batch_end]

                # Create tasks for this batch
                tasks = []
                for topic_id, institution_id in batch_combinations:
                    tasks.append(
                        self._process_institution_based_searches(
                            topic_id, institution_id
                        )
                    )

                # Run batch in parallel
                batch_results = await asyncio.gather(*tasks)

                # Add results to the main list
                self.institution_based_searches.extend(batch_results)

                # Update progress bar
                pbar.update(len(batch_combinations))

                # Optional: Add a small delay between batches to be respectful to APIs
                if batch_start + batch_size < len(all_combinations):
                    await asyncio.sleep(0.1)

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
        title = "Professor | Researcher | Scientist"
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

                                topic_keywords = topic.get("keywords")
                                topic_domain = topic.get("domain").get("display_name")
                                topic_field = topic.get("field").get("display_name")
                                topic_subfield = topic.get("subfield").get(
                                    "display_name"
                                )
                                topic_name = (
                                    topic.get("display_name")
                                    if not topic_subfield
                                    else f"{topic.get('display_name')} ({topic_subfield})"
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
            where_query=f"{city}, {COUNTRIES[country_code]}",
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
        title = "Professor | Researcher | Scientist"
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

                                topic_keywords = topic.get("keywords")
                                topic_domain = topic.get("domain").get("display_name")
                                topic_field = topic.get("field").get("display_name")
                                topic_subfield = topic.get("subfield").get(
                                    "display_name"
                                )
                                topic_name = (
                                    topic.get("display_name")
                                    if not topic_subfield
                                    else f"{topic.get('display_name')} ({topic_subfield})"
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
            .filter(authorships={"institutions.id": institution_id})
            .filter(topics={"id": topic_id})
            .get()
        )

        leads = []
        title = "Professor | Researcher | Scientist"
        topic_name = ""
        institution_name = ""
        openalex_results = None
        selected_authors = set()
        institution_country = ""

        for record in query_results:
            if record.get("authorships", []):
                for authorship in record.get("authorships", []):
                    if authorship.get("institutions", []):
                        for inst in authorship.get("institutions", []):
                            if inst.get("id") == institution_id:
                                # getting relevant openalex data
                                topic = record.get("primary_topic", {})

                                topic_keywords = topic.get("keywords")
                                topic_domain = topic.get("domain").get("display_name")
                                topic_field = topic.get("field").get("display_name")
                                topic_subfield = topic.get("subfield").get(
                                    "display_name"
                                )
                                topic_name = (
                                    topic.get("display_name")
                                    if not topic_subfield
                                    else f"{topic.get('display_name')} ({topic_subfield})"
                                )

                                institution_name_alternatives = inst.get(
                                    "display_name_alternatives", []
                                )
                                institution_name = (
                                    inst.get("display_name")
                                    if not institution_name_alternatives
                                    else f"{inst.get('display_name')} (also known as {', '.join(institution_name_alternatives)})"
                                )
                                institution_country = inst.get("country_code")
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
            where_query=COUNTRIES[institution_country],
        )
        query_string = build_final_query(research_params, True, institution_name)

        sample = Sample(
            query_params=research_params,
            query_string=query_string,
            query_type=QueryType.INSTITUTION_FOCUSED,
            expected_results=LeadResults(leads=leads),
            openalex_results=openalex_results,
        )

        return sample


async def main():
    """Example usage of the synthetic query generator with checkpointing"""
    config = GenerationConfig(
        target_queries=100,  # Start with smaller number for testing
        batch_size=10,
        max_results_per_query=5,
        checkpoint_dir="notebooks/checkpoints/synthetic_queries",
        output_file="notebooks/synthetic_queries_sample.json",
    )

    generator = SyntheticQueryGenerator(config)

    try:
        results = await generator.generate_queries()

        print(f"\nGenerated {len(results)} synthetic queries!")

        # Show a few examples
        print("\nSample queries:")
        for i, result in enumerate(results[:3]):
            print(f"\n{i + 1}. {result.query_string}")
            print(f"   Found {len(result.expected_results.leads)} leads")
            if result.expected_results.leads:
                print(f"   Sample lead: {result.expected_results.leads[0].name}")

    except KeyboardInterrupt:
        print(
            "\n[yellow]Process interrupted. Progress has been saved and can be resumed.[/yellow]"
        )
    except Exception as e:
        print(f"\n[red]Error occurred: {e}[/red]")
        print("[yellow]Check checkpoints for recovery.[/yellow]")
        raise


if __name__ == "__main__":
    asyncio.run(main())

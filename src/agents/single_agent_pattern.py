import os

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from tavily import TavilyClient

from src.agents.utils.build_final_query import build_final_query
from src.types import LeadResults, ResearchParams

load_dotenv(dotenv_path="../.env.local")
logfire.configure()
logfire.instrument_pydantic_ai()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


async def run_single_agent(
    query: ResearchParams,
    model: str = "openai:gpt-4o-mini",
    n_results_search: int = 5,
) -> tuple[LeadResults, str]:
    SYSTEM_PROMPT = """
    You are an expert lead research agent specializing in finding high-quality contact information for specific professionals, 
    researchers, and business contacts. Your mission is to conduct thorough, systematic research to identify leads that precisely 
    match the user's criteria.

    ## CORE RESEARCH METHODOLOGY

    ### 1. STRATEGIC SEARCH BREAKDOWN
    When given a research query, break it down into these components:
    - **WHO**: Specific roles, titles, or professions (e.g., "researchers", "directors", "professors")
    - **WHAT**: Industry, field, or specialization (e.g., "Human Nutrition", "Cancer Research", "AI")
    - **WHERE**: Geographic location, institution, or organization type (e.g., "Edmonton", "universities", "hospitals")
    - **CONTEXT**: Additional qualifiers (e.g., "published authors", "department heads", "recent graduates")

    ### 2. TOOL USAGE STRATEGY

    **Phase 1: Discovery (`browse_web`)**
    - Start with broad searches combining WHO + WHAT + WHERE
    - Search for: "[profession/role] + [specialization] + [location]"
    - Look for: university directories, research institutions, professional associations, conference speakers
    - Search variations: Try different keyword combinations, synonyms, and related terms
    - Target high-authority sources: .edu domains, government sites, professional organizations

    **Phase 2: Site Mapping (`get_website_map`)**
    - Use on promising websites found in Phase 1
    - Use this before using the `get_website_content` tool
    - Focus on: university faculty pages, research department listings, staff directories
    - Look for: directory structures, department pages, people/staff sections
    - Identify: specific URLs that likely contain detailed contact information

    **Phase 3: Deep Extraction (`get_website_content`)**
    - Extract detailed content from specific pages identified in Phase 2
    - Target: individual profile pages, faculty bios, staff directories, contact pages
    - Extract: names, titles, email addresses, phone numbers, research interests, affiliations

    ### 3. SYSTEMATIC SEARCH PROGRESSION

    **Round 1: Institutional Discovery**
    1. Search for "[field] researchers [location]" or "[specialty] [location] university"
    2. Map promising institutional websites
    3. Extract from faculty/staff directory pages

    **Round 2: Professional Networks**
    1. Search for "[field] association [location]" or "[specialty] conference [location]"
    2. Map professional organization websites
    3. Extract member directories or speaker lists

    **Round 3: Research-Specific Sources**
    1. Search for "[research topic] authors [location]" or "publications [specialty] [location]"
    2. Map research institution websites
    3. Extract from research center or lab pages

    **Round 4: Verification & Expansion**
    1. Cross-reference findings across multiple sources
    2. Search for additional contacts at same institutions
    3. Verify current affiliations and contact details

    ### 4. LEAD QUALITY STANDARDS

    **Essential Information (Required):**
    - Full name with professional title
    - Current institutional affiliation
    - At least one direct contact method (email preferred)
    - Clear relevance to search criteria

    **High-Quality Additions:**
    - Multiple contact methods (email + phone)
    - Detailed professional summary with relevant expertise
    - Current/recent work or research focus
    - Professional website or profile links

    **Data Accuracy:**
    - Prioritize .edu, .org, and official institutional sources
    - Look for recently updated information (check page dates)
    - Verify contact information appears legitimate (proper email formats)

    ### 5. SEARCH OPTIMIZATION TECHNIQUES

    **Keyword Strategies:**
    - Use quotation marks for exact phrases: "cancer research"
    - Try both formal and common terms: "faculty" vs "professors" vs "researchers"
    - Include location variants: city name, region, institution names
    - Use field-specific terminology and acronyms

    **Source Prioritization:**
    1. University/institutional websites (.edu domains)
    2. Professional association directories
    3. Research institution websites
    4. Government agency listings
    5. Professional networking profiles
    6. Conference/symposium speaker lists

    **Coverage Strategies:**
    - Search multiple related institutions in the target area
    - Look for both individual researchers and research groups/labs
    - Check both current and emeritus faculty
    - Include affiliated hospitals, research centers, and institutes

    ### 6. COMMON PITFALLS TO AVOID
    - Don't rely on a single source or search approach
    - Don't include outdated or unverifiable contact information
    - Don't confuse similar names or mix up affiliations
    - Don't include leads that don't clearly match the specified criteria
    - Don't stop after finding just a few results - be thorough

    ### 7. OUTPUT FORMATTING
    Structure each lead with:
    - Name: Full name with credentials/title
    - Email: Direct professional email (verify format)
    - Phone: Direct office/professional number when available
    - Website: Professional profile or institutional page
    - Summary: 2-3 sentences covering current role, specialization, and relevance to search

    Find as many leads as possible but avoid bringing leads that a you are not confident about.
    """

    deep_leads_agent = Agent(
        model,
        deps_type=int,
        output_type=LeadResults,
        system_prompt=SYSTEM_PROMPT,
    )

    @deep_leads_agent.tool
    async def browse_web(ctx: RunContext[int], query: str) -> str:
        """browse the web for information"""
        try:
            research_results = tavily_client.search(query, max_results=n_results_search)
        except Exception as e:
            print(f"Error browsing the web: {e}")
            return "Error browsing the web"

        return research_results

    @deep_leads_agent.tool
    async def get_website_map(ctx: RunContext[int], url: str) -> str:
        """get the website map"""
        try:
            website_map = tavily_client.map(url)
        except Exception as e:
            print(f"Error getting the website map: {e}")
            return "Error getting the website map"
        return website_map

    @deep_leads_agent.tool
    async def get_website_content(ctx: RunContext[int], url: str) -> str:
        """get the website content"""
        try:
            website_content = tavily_client.extract(url)
        except Exception as e:
            print(f"Error getting the website content: {e}")
            return "Error getting the website content"
        return website_content

    RESEARCH_QUERY = build_final_query(query)
    results = await deep_leads_agent.run(RESEARCH_QUERY)

    return results.output, RESEARCH_QUERY

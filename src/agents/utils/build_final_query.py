from textwrap import dedent
from typing import Optional

from src.types import ResearchParams


def build_final_query(
    params: ResearchParams,
    is_institution: bool = False,
    institution_name: Optional[str] = None,
) -> str:
    if is_institution:
        # For institutions, format as: institution name, country
        final_query = dedent(f"""
        Find me as many leads as possible for the following query:
        
        Who: {params.who_query}
        What is the field of study: {params.what_query}
        Where are they located geographically (institution name, geographic location): {institution_name}, {params.where_query}
        Additional context (ignore if None): {params.context_query}
        
        """)
    else:
        final_query = dedent(f"""
            Find me as many leads as possible for the following query:
            
            Who: {params.who_query}
            What is the field of study: {params.what_query}
            Where are they located geographically (geographic location): {params.where_query}
            Additional context (ignore if None): {params.context_query}
            
            """)
    return final_query

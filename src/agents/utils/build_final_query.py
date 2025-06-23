from src.types import ResearchParams


def build_final_query(params: ResearchParams) -> str:
    final_query = f"""
        Find me as many leads as possible for the following query:
        
        Who: {params.who_query}
        What is the field of study: {params.what_query}
        Where are they located: {params.where_query}
        Additional context: {params.context_query}
        """
    return final_query

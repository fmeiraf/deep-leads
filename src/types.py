from typing import Optional

from pydantic import BaseModel, Field


class ResearchParams(BaseModel):
    who_query: str = Field(
        description="Specific roles, titles, or professions (e.g., 'researchers', 'directors', 'professors')"
    )
    what_query: str = Field(
        description="Industry, field, or specialization (e.g., 'Human Nutrition', 'Cancer Research', 'AI')"
    )
    where_query: Optional[str] = Field(
        description="Geographic location, institution, or organization type (e.g., 'Edmonton', 'universities', 'hospitals')",
        default=None,
    )
    context_query: Optional[str] = Field(
        description="Additional qualifiers (e.g., 'published authors', 'department heads', 'recent graduates')",
        default=None,
    )


class Lead(BaseModel):
    name: str = Field(
        description="The name of the person (exclude any titles or degrees like PhD, MD, etc.)",
    )
    email: Optional[str] = None
    title: Optional[str] = Field(
        description="The professional title of the person (e.g. Professor, Associate Professor, Assistant Professor, etc.)",
        default=None,
    )
    headline: Optional[str] = Field(
        description="The headline of the person (e.g. Professor at Univerisity X at Department Y, Associate Professor, Assistant Professor, etc.)",
        default=None,
    )
    phone: Optional[str] = None
    website: Optional[str] = None
    background_summary: Optional[str] = Field(
        description="A short summary of the person's background, research interests, and publications",
        default=None,
    )
    source_url: Optional[str] = Field(
        description="The url where the information was found",
        default=None,
    )


class LeadResults(BaseModel):
    leads: list[Lead]


class EvalParams(BaseModel):
    query_params: ResearchParams
    expected_results: list[Lead] = Field(
        description="The expected results of the query",
    )

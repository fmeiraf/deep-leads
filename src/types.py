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
        description="The name of the person (exclude any titles or degrees like PhD, MD, Dr., professional titles, etc.)",
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

    def to_string(self) -> str:
        """
        Converts the Lead instance to a readable string representation.
        """
        data = self.model_dump()
        lines = []

        if data.get("name"):
            lines.append(f"Name: {data['name']}")
        if data.get("title"):
            lines.append(f"Title: {data['title']}")
        if data.get("headline"):
            lines.append(f"Headline: {data['headline']}")
        if data.get("email"):
            lines.append(f"Email: {data['email']}")
        if data.get("phone"):
            lines.append(f"Phone: {data['phone']}")
        if data.get("website"):
            lines.append(f"Website: {data['website']}")
        if data.get("background_summary"):
            lines.append(f"Background: {data['background_summary']}")
        if data.get("source_url"):
            lines.append(f"Source: {data['source_url']}")

        return "\n".join(lines)

    def __str__(self) -> str:
        """
        String representation of the Lead instance.
        """
        return self.to_string()


class LeadResults(BaseModel):
    leads: list[Lead]

    def to_string(self) -> str:
        """
        Converts all leads in the results to a readable string representation.
        """
        if not self.leads:
            return "No leads found."

        lead_strings = [lead.to_string() for lead in self.leads]
        return "\n\n".join(lead_strings)

    def __str__(self) -> str:
        """
        String representation of the LeadResults instance.
        """
        return self.to_string()


class ResearcherResults(BaseModel):
    task: str = Field(
        description="The task that the researcher was assigned",
    )
    search_strategy: str = Field(
        description="The search strategy that the researcher used",
    )
    leads: list[Lead]

    def to_string(self) -> str:
        """
        Converts all leads in the results to a readable string representation.
        """
        if not self.leads:
            return "No leads found."

        lead_strings = [lead.to_string() for lead in self.leads]
        return "\n\n".join(lead_strings)


class EvalParams(BaseModel):
    query_params: ResearchParams
    expected_results: LeadResults = Field(
        description="The expected results of the query",
    )

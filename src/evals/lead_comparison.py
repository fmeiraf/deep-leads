from typing import List, Tuple

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.types import Lead

console = Console()


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, remove extra spaces)"""
    if not text:
        return ""
    return text.lower().strip().replace("  ", " ")


def leads_match(lead1: Lead, lead2: Lead) -> bool:
    """Check if two leads match based on name or email"""
    # Normalize both leads' name and email
    lead1_name = normalize_text(lead1.name) if lead1.name else ""
    lead1_email = normalize_text(lead1.email) if lead1.email else ""
    lead2_name = normalize_text(lead2.name) if lead2.name else ""
    lead2_email = normalize_text(lead2.email) if lead2.email else ""

    # Match if either name or email matches (and is not empty)
    name_match = lead1_name and lead2_name and lead1_name == lead2_name
    email_match = lead1_email and lead2_email and lead1_email == lead2_email

    return name_match or email_match


def find_lead_matches(
    actual_leads: List[Lead], expected_leads: List[Lead]
) -> Tuple[List[Tuple[Lead, Lead]], List[Lead], List[Lead]]:
    """
    Compare actual vs expected leads and return:
    - matches: List of (actual_lead, expected_lead) tuples
    - missing: Expected leads not found in actual
    - extra: Actual leads not found in expected

    Leads match if either their names or emails match.
    """
    matches = []
    missing = []
    extra = []

    # Keep track of which actual leads have been matched
    matched_actual_indices = set()

    # Find matches and missing
    for expected_lead in expected_leads:
        found_match = False

        for i, actual_lead in enumerate(actual_leads):
            # Skip if this actual lead is already matched
            if i in matched_actual_indices:
                continue

            if leads_match(actual_lead, expected_lead):
                matches.append((actual_lead, expected_lead))
                matched_actual_indices.add(i)
                found_match = True
                break

        if not found_match:
            missing.append(expected_lead)

    # Find extra leads (actual leads that weren't matched)
    for i, actual_lead in enumerate(actual_leads):
        if i not in matched_actual_indices:
            extra.append(actual_lead)

    return matches, missing, extra


def create_lead_table(leads: List[Lead], title: str, color: str) -> Table:
    """Create a rich table for displaying leads"""
    table = Table(
        title=f"[{color}]{title}[/{color}]",
        show_header=True,
        header_style=f"bold {color}",
    )
    table.add_column("Name", style="bold")
    table.add_column("Title", max_width=25)
    table.add_column("Email", max_width=30)
    table.add_column("Phone", max_width=15)
    table.add_column("Website", max_width=30)

    for lead in leads:
        table.add_row(
            lead.name or "N/A",
            lead.title or "N/A",
            lead.email or "N/A",
            lead.phone or "N/A",
            lead.website or "N/A",
        )

    return table


def create_match_comparison_table(matches: List[Tuple[Lead, Lead]]) -> Table:
    """Create a comparison table showing actual vs expected for matches"""
    table = Table(
        title="[green]✓ MATCHED LEADS - COMPARISON[/green]",
        show_header=True,
        header_style="bold green",
    )
    table.add_column("Field", style="bold")
    table.add_column("Actual", style="cyan")
    table.add_column("Expected", style="yellow")
    table.add_column("Match", justify="center")

    for actual_lead, expected_lead in matches:
        # Add separator row
        table.add_row("─" * 20, "─" * 30, "─" * 30, "─" * 10)
        table.add_row(f"[bold]{actual_lead.name}[/bold]", "", "", "")

        # Compare each field
        fields_to_compare = [
            ("Name", actual_lead.name, expected_lead.name),
            ("Title", actual_lead.title, expected_lead.title),
            ("Email", actual_lead.email, expected_lead.email),
            ("Phone", actual_lead.phone, expected_lead.phone),
            ("Website", actual_lead.website, expected_lead.website),
        ]

        for field_name, actual_val, expected_val in fields_to_compare:
            actual_str = actual_val or "N/A"
            expected_str = expected_val or "N/A"

            # Check if values match (case insensitive for strings)
            if actual_val and expected_val:
                match = (
                    "✓"
                    if str(actual_val).lower().strip()
                    == str(expected_val).lower().strip()
                    else "✗"
                )
                match_color = "green" if match == "✓" else "red"
            elif actual_val == expected_val:  # Both None
                match = "✓"
                match_color = "green"
            else:
                match = "✗"
                match_color = "red"

            table.add_row(
                field_name,
                actual_str,
                expected_str,
                f"[{match_color}]{match}[/{match_color}]",
            )

    return table


def display_leads_comparison(
    actual_leads: List[Lead], expected_leads: List[Lead]
) -> None:
    """Display a comprehensive comparison of actual vs expected leads"""

    matches, missing, extra = find_lead_matches(actual_leads, expected_leads)

    # Summary statistics
    total_expected = len(expected_leads)
    total_actual = len(actual_leads)
    total_matches = len(matches)
    total_missing = len(missing)
    total_extra = len(extra)

    # Create summary panel
    summary_text = Text()
    summary_text.append("LEAD COMPARISON SUMMARY\n\n", style="bold white")
    summary_text.append(f"Expected Leads: {total_expected}\n", style="yellow")
    summary_text.append(f"Actual Leads: {total_actual}\n", style="cyan")
    summary_text.append(f"✓ Matches: {total_matches}\n", style="green")
    summary_text.append(f"✗ Missing: {total_missing}\n", style="red")
    summary_text.append(f"⚠ Extra: {total_extra}\n", style="orange3")

    if total_expected > 0:
        recall = (total_matches / total_expected) * 100
        summary_text.append(f"\nRecall: {recall:.1f}%", style="bold white")

    summary_panel = Panel(
        summary_text, title="[bold]Summary[/bold]", border_style="white"
    )
    console.print(summary_panel)
    console.print()

    # Display matches with detailed comparison
    if matches:
        console.print(create_match_comparison_table(matches))
        console.print()

    # Display missing and extra leads side by side
    panels = []

    if missing:
        missing_table = create_lead_table(
            missing, f"✗ MISSING LEADS ({len(missing)})", "red"
        )
        panels.append(Panel(missing_table, border_style="red"))

    if extra:
        extra_table = create_lead_table(
            extra, f"⚠ EXTRA LEADS ({len(extra)})", "orange3"
        )
        panels.append(Panel(extra_table, border_style="orange3"))

    if panels:
        if len(panels) == 2:
            console.print(Columns(panels, equal=True))
        else:
            for panel in panels:
                console.print(panel)
        console.print()

    # Display separator before evaluation
    console.print("─" * 80, style="dim white")
    console.print("[bold white]Starting Evaluation...[/bold white]")
    console.print("─" * 80, style="dim white")
    console.print()

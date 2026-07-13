"""
report.py
---------
Day 1-2: Report command routing setup
Week 3 me actual reporting logic aayegi
"""

import typer
from rich.console import Console

report_app = typer.Typer(help="Generate and export cost-saving reports.")
console = Console()


@report_app.command("export")
def export_report():
    """
    Export report as CSV/JSON.implemented in week 3
    """
    console.print("[yellow]Report export Week 3  add .[/yellow]")


@report_app.command("summary")
def summary_report():
    """
    
    Show cost saving summary.implemented in week 3
    """
    console.print("[yellow]⚠ Summary report Week 3  add .[/yellow]")
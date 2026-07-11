"""
report.py
---------
Sub-command group for generating and exporting reports.
Actual reporting logic will be implemented in Week 3.
"""

import typer
from rich.console import Console

report_app = typer.Typer(help="Commands to generate and export cost-saving reports.")
console = Console()


@report_app.command("export")
def export_report():
    """
    (Week 3 me implement hoga) Export report as CSV/JSON.
    """
    console.print("[yellow]⚠ Report export logic Week 3 me add hogi.[/yellow]")
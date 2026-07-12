
"""
Cloud Infrastructure Auditor & Cost Optimizer (CLI)
-----------------------------------------------------
Entry point for the CLI application.

Week 1 - Day 1-2:
- Setup CLI framework using Typer
- Establish command routing structure
"""

import typer
from rich.console import Console

# Import command groups (sub-apps) that will be built in later days/weeks
from app.commands import scan, report

# Main Typer app object
app = typer.Typer(
    name="cloud-auditor",
    help="🔍 Cloud Infrastructure Auditor & Cost Optimizer - Scan, Audit, and Save Cloud Costs.",
    add_completion=False,
)

console = Console()

# ---- Command Routing Structure ----
# Har feature ka apna alag sub-command group hoga.
# Example future usage: `cloud-auditor scan ebs` , `cloud-auditor report export`
app.add_typer(scan.scan_app, name="scan", help="Scan cloud resources for waste/misconfigurations")
app.add_typer(report.report_app, name="report", help="Generate and export cost-saving reports")


@app.command()
def version():
    """
    Show the current version of the tool.
    """
    console.print("[bold green]Cloud Infrastructure Auditor[/bold green] - v0.1.0 (Day 1-2 Setup)")


@app.command()
def hello():
    """
    Simple test command to confirm CLI is working.
    """
    console.print("[bold cyan]✅ CLI framework is up and running![/bold cyan]")


if __name__ == "__main__":
    app()
main.py
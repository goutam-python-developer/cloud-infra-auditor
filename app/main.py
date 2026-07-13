
"""
Cloud Infrastructure Auditor & Cost Optimizer (CLI)
-----------------------------------------------------
Entry point for the CLI application.

Week 1 - Day 1-5:
- Setup CLI framework using Typer
- Boto3+ Credential connected
"""

import typer
from rich.console import Console
from app.commands import scan, report
from app.config import grt_aws_session, assume_role, get_local_profiles

# Main Typer app object
app = typer.Typer(
    name="cloud-auditor",
    help=" Cloud Infrastructure Auditor & Cost Optimizer - Scan, Audit, and Save Cloud Costs.",
    add_completion=False,
)

console = Console()

app.add_typer(scan.scan_app, name="scan", help="Scan cloud resources ")
app.add_typer(report.report_app, name="report", help="Generate and export cost-saving reports")


@app.command()
def version():
    console.print("[bold green]Cloud Infrastructure Auditor[/bold green] - v0.1.0 ")


@app.command()
def connect(
    profile: str = typer.Option("default", help="AWS Profile naam"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    
    console.print(f"[cyan] Connecting: profile={profile}, region={region}[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        console.print("[green]Connected![/green]")
    else:
        console.print("[red] Connection fail![/red]")


@app.command()
def profiles():
    """
    Day 5: Local AWS profiles list 
    """
    console.print("[cyan] Local AWS Profiles:[/cyan]")
    get_local_profiles()


@app.command()
def hello():
    
    console.print("[bold cyan] CLI framework is up and running![/bold cyan]")


if __name__ == "__main__":
    app()
main.py

"""
Cloud Infrastructure Auditor & Cost Optimizer (CLI)
-----------------------------------------------------
Entry point for the CLI application.

Week 1 - Day 1-7 Complete:
CLI + Boto3 + Credential+ Regions


week 2 - Day 1-2 
EBS+ Elastic IP scanning added
"""

import typer
from rich.console import Console
from app.commands import scan, report
from app.config import get_aws_session, assume_role, get_local_profiles
from app.regions import get_all_regions, safe_api_call

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
def hello():
    "show current version."
    console.print("[bold cyan]CLI is running ![/bold cyan]")

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
def regions(
    profile: str = typer.Option("default", help="AWS Profile naam")
):
    """Day 6: All AWS regions fetch ."""
    console.print("[cyan] Regions fetch are processing...[/cyan]")
    session = get_aws_session(profile=profile)
    if session:
        all_regions = get_all_regions(session)
        console.print(f"[green] Regions: {all_regions}[/green]")
    else:
        console.print("[red] Session fail![/red]")

@app.command()
def test_api():
    console.print("[cyan]API Rate Limit Handler Test processing...[/cyan]")
    
    def sample_call():
        console.print("[green] API Call successful![/green]")
        return "success"
    
    result = safe_api_call(sample_call)
    
    if result:
        console.print("[green]safe_api_call are working![/green]")
    else:
        console.print("[red] API call fail![/red]")
@app.command()
def scan_all(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 3: directly full scan to main.
    """
    from app.scanner import scan_all_resources
    console.print("[cyan] Full Scan main start[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        results = scan_all_resources(session, region)
        console.print(f"[yellow]EBS: {len(results['ebs'])} | EIP: {len(results['eip'])}[/yellow]")
    else:
        console.print("[red] Session fail![/red]")



if __name__ == "__main__":
    app()
main.py
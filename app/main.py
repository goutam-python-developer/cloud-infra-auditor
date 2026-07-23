
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

@app.command()
def ec2_detailed(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 5: EC2 detailed scanning in main.
    """
    from app.scanner import scan_ec2_detailed
    console.print("[cyan] EC2 Detailed Scan starting[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        results = scan_ec2_detailed(session, region)
        console.print(f"[yellow]Total EC2: {len(results)}[/yellow]")
        underutilized = [r for r in results if r["Underutilized"]]
        console.print(f"[red]Underutilized: {len(underutilized)}[/red]")
    else:
        console.print("[red] Session fail![/red]")

@app.command()
def ec2_regions(
    profile: str = typer.Option("default", help="AWS Profile")
):
    """
    Day 6: Multiple regions scanning in EC2 .
    """
    from app.scanner import scan_all_ec2_regions
    console.print("[cyan] Multi-Region EC2 Scanning.[/cyan]")
    session = get_aws_session(profile=profile)
    if session:
        results = scan_all_ec2_regions(session)
        for region, instances in results.items():
            console.print(
                f"[yellow]Region: {region} | "
                f"Underutilized EC2: {len(instances)}[/yellow]"
            )
    else:
        console.print("[red] Session fail![/red]") 

@app.command()
def store_all(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 7: All scan data store 
    """
    from app.scanner import (
        scan_unattached_ebs,
        scan_unassociated_eip,
        scan_underutilized_ec2,
        store_scan_results
    )
    console.print("[cyan] Full Scan and Store starting[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        ebs = scan_unattached_ebs(session, region)
        eip = scan_unassociated_eip(session, region)
        ec2 = scan_underutilized_ec2(session, region)
        data = store_scan_results(ebs, eip, ec2, region)
        console.print(
            f"[green] Data Stored! "
            f"Total Issues: {data['metadata']['total_issues']}[/green]"
        )
    else:
        console.print("[red] Session fail![/red]")


@app.command()
def show_report(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Week 3 Day 1:  Show report in Rich tables.
    """
    from app.scanner import generate_report_data
    from app.commands.report import (
        print_ebs_table,
        print_eip_table,
        print_ec2_table,
        print_summary_table
    )
    console.print("[cyan] Report generating starting[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        report_data = generate_report_data(session, region)
        print_ebs_table(report_data["ebs_volumes"])
        print_eip_table(report_data["elastic_ips"])
        print_ec2_table(report_data["ec2_instances"])
        print_summary_table(report_data)
    else:
        console.print("[red]Session fail![/red]")

@app.command()
def show_costs(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Week 3 Day 2: Cost savings table showing
    """
    from app.scanner import generate_report_data, estimate_cost_savings
    from app.commands.report import print_cost_savings_table
    console.print("[cyan] Cost Savings Reporting[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        report_data = generate_report_data(session, region)
        savings = estimate_cost_savings(report_data)
        print_cost_savings_table(savings)
    else:
        console.print("[red] Session fail![/red]")


@app.command()
def full_report(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Week 3 Day 3: show  fully report.
    """
    from app.scanner import generate_full_report
    from app.commands.report import print_full_report
    console.print("[cyan] Full Report generating...[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        full_report_data = generate_full_report(session, region)
        print_full_report(full_report_data)
    else:
        console.print("[red]Session fail![/red]")


@app.command()
def export_csv(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region"),
    output: str = typer.Option("reports", help="Output folder")
):
    """
    Week 3 Day 4: CSV exporting.
    """
    from app.scanner import generate_full_report, prepare_csv_data
    from app.commands.report import export_to_csv
    console.print("[cyan] CSV Export starting...[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        full_report_data = generate_full_report(session, region)
        csv_data = prepare_csv_data(full_report_data)
        export_to_csv(csv_data, output)
    else:
        console.print("[red] Session fail![/red]")


if __name__ == "__main__":
    app()
main.py
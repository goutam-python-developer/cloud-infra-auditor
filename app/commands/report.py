"""
report.py
---------
Week 3 - Day 1-3:
creating beautiful formatted
tables and reports using Rich library
"""

import typer
from rich.console import Console
from rich.table import Table
from rich import box
from app.config import get_aws_session

report_app = typer.Typer(help="Generate and export cost-saving reports.")
console = Console()


def print_ebs_table(ebs_results):
    """
    Day 1: printing  EBS results in Rich table .
    """
    table = Table(
        title=" Unattached EBS Volumes",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold red"
    )

    table.add_column("Volume ID", style="cyan")
    table.add_column("Size (GB)", style="yellow")
    table.add_column("Type", style="green")
    table.add_column("Region", style="blue")

    for ebs in ebs_results:
        table.add_row(
            ebs["VolumeId"],
            str(ebs["Size"]),
            ebs["Type"],
            ebs["Region"]
        )

    console.print(table)


def print_eip_table(eip_results):
    """
    Day 1: printing EIP results in Rich table.
    """
    table = Table(
        title="Idle Elastic IPs",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold red"
    )

    table.add_column("Public IP", style="cyan")
    table.add_column("Allocation ID", style="yellow")
    table.add_column("Region", style="blue")

    for eip in eip_results:
        table.add_row(
            eip["PublicIp"],
            eip["AllocationId"],
            eip["Region"]
        )

    console.print(table)


def print_ec2_table(ec2_results):
    """
    Day 1:Print EC2 results in  Rich table.
    """
    table = Table(
        title=" Underutilized EC2 Instances",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold red"
    )

    table.add_column("Instance ID", style="cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Avg CPU %", style="green")
    table.add_column("Region", style="blue")

    for ec2 in ec2_results:
        table.add_row(
            ec2["InstanceId"],
            ec2["InstanceType"],
            str(ec2["AvgCPU"]),
            ec2["Region"]
        )

    console.print(table)


def print_summary_table(report_data):
    """
    Day 1: Summary table printing
    """
    table = Table(
        title=" Cost Saving Summary Report",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold green"
    )

    table.add_column("Resource Type", style="cyan")
    table.add_column("Issues Found", style="red")

    table.add_row(
        "Unattached EBS Volumes",
        str(report_data["metadata"]["summary"]["unattached_ebs"])
    )
    table.add_row(
        "Idle Elastic IPs",
        str(report_data["metadata"]["summary"]["idle_eips"])
    )
    table.add_row(
        "Underutilized EC2",
        str(report_data["metadata"]["summary"]["underutilized_ec2"])
    )
    table.add_row(
        "Total Issues",
        str(report_data["metadata"]["total_issues"])
    )

    console.print(table)


@report_app.command("show")
def show_report(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 1: Show report in Beautiful Rich tables .
    """
    console.print("[cyan] Report generate starting[/cyan]")
    session = get_aws_session(profile=profile, region=region)

    if session:
        from app.scanner import generate_report_data
        report_data = generate_report_data(session, region)

        # Tables print karo
        print_ebs_table(report_data["ebs_volumes"])
        print_eip_table(report_data["elastic_ips"])
        print_ec2_table(report_data["ec2_instances"])
        print_summary_table(report_data)

    else:
        console.print("[red] Session fail![/red]")


@report_app.command("export")
def export_report():
    """
   implemeningt in   Day 4-5 
    Export report as CSV/JSON.
    """
    console.print("[yellow] Export adding in Week 3 Day 4-5 .[/yellow]")


@report_app.command("summary")
def summary_report():
    """
    Day 1: show Summary table 
    """
    console.print("[yellow] Summary adding in Week 3 Day 4-5  .[/yellow]")
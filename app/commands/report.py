"""
report.py
---------
Week 3 - Day 1-3:
creating beautiful formatted
tables and reports using Rich library
"""
import csv
import os

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



def print_cost_savings_table(savings):
    """
    Day 2: Cost savings print in   Rich table 
    """
    table = Table(
        title=" Estimated Monthly Cost Savings",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold green"
    )

    table.add_column("Resource Type", style="cyan")
    table.add_column("Estimated Savings/Month", style="green")

    table.add_row(
        "Unattached EBS Volumes",
        f"${savings['ebs_savings']:.2f}"
    )
    table.add_row(
        "Idle Elastic IPs",
        f"${savings['eip_savings']:.2f}"
    )
    table.add_row(
        "Underutilized EC2",
        f"${savings['ec2_savings']:.2f}"
    )
    table.add_row(
        " Total Savings",
        f"${savings['total_savings']:.2f}"
    )

    console.print(table)


@report_app.command("costs")
def show_cost_savings(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 2: Cost savings table show.
    """
    console.print("[cyan] Cost Savings calculating[/cyan]")
    session = get_aws_session(profile=profile, region=region)

    if session:
        from app.scanner import generate_report_data, estimate_cost_savings
        report_data = generate_report_data(session, region)
        savings = estimate_cost_savings(report_data)
        print_cost_savings_table(savings)
    else:
        console.print("[red] Session fail![/red]")    



def print_full_report(full_report):
    """
    Day 3: print all  report.
    Showing all tables .
    """
    console.print("\n")
    console.rule("[bold cyan] Cloud Infrastructure Audit Report[/bold cyan]")
    console.print("\n")

    # EBS Table
    print_ebs_table(full_report["ebs_volumes"])
    console.print("\n")

    # EIP Table
    print_eip_table(full_report["elastic_ips"])
    console.print("\n")

    # EC2 Table
    print_ec2_table(full_report["ec2_instances"])
    console.print("\n")

    # Summary Table
    print_summary_table(full_report)
    console.print("\n")

    # Cost Savings Table
    print_cost_savings_table(full_report["cost_savings"])
    console.print("\n")

    console.rule("[bold green]Report Complete[/bold green]")


@report_app.command("full")
def full_report(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 3: showing  full report.
    EBS + EIP + EC2 + Cost Savings.
    """
    console.print("[cyan] Full Report generating...[/cyan]")
    session = get_aws_session(profile=profile, region=region)

    if session:
        from app.scanner import generate_full_report
        full_report_data = generate_full_report(session, region)
        print_full_report(full_report_data)
    else:
        console.print("[red]Session fail![/red]")


        
def export_to_csv(csv_data, output_dir: str = "reports"):
    """
    Day 4: Data ko CSV files me export karo.
    """
    # Reports folder banao
    os.makedirs(output_dir, exist_ok=True)

    # EBS CSV
    if csv_data["ebs"]:
        ebs_file = os.path.join(output_dir, "ebs_report.csv")
        with open(ebs_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=csv_data["ebs"][0].keys()
            )
            writer.writeheader()
            writer.writerows(csv_data["ebs"])
        console.print(f"[green] EBS Report saved: {ebs_file}[/green]")

    # EIP CSV
    if csv_data["eip"]:
        eip_file = os.path.join(output_dir, "eip_report.csv")
        with open(eip_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=csv_data["eip"][0].keys()
            )
            writer.writeheader()
            writer.writerows(csv_data["eip"])
        console.print(f"[green]EIP Report saved: {eip_file}[/green]")

    # EC2 CSV
    if csv_data["ec2"]:
        ec2_file = os.path.join(output_dir, "ec2_report.csv")
        with open(ec2_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=csv_data["ec2"][0].keys()
            )
            writer.writeheader()
            writer.writerows(csv_data["ec2"])
        console.print(f"[green] EC2 Report saved: {ec2_file}[/green]")

    console.print(f"[cyan] All CSV files '{output_dir}'  in folder ![/cyan]")


@report_app.command("export-csv")
def export_csv(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region"),
    output: str = typer.Option("reports", help="Output folder naam")
):
    """
    Day 4: Scan results exporting in CSV.
    """
    console.print("[cyan] CSV Export starting...[/cyan]")
    session = get_aws_session(profile=profile, region=region)

    if session:
        from app.scanner import generate_full_report, prepare_csv_data
        full_report_data = generate_full_report(session, region)
        csv_data = prepare_csv_data(full_report_data)
        export_to_csv(csv_data, output)
    else:
        console.print("[red] Session fail![/red]")      
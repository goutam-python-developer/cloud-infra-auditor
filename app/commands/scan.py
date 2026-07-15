"""
scan.py
-------
Week 2 - Day 1-3:
EBS aur Elastic IP scan commands
"""

import typer
from rich.console import Console
from app.scanner import scan_unattached_ebs, scan_unassociated_eip
from app.config import get_aws_session

scan_app = typer.Typer(help="Scan AWS resources for waste.")
console = Console()


@scan_app.command("ebs")
def scan_ebs(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 1: Unattached EBS volumes scan karo.
    """
    console.print("[cyan]EBS Scan start[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        results = scan_unattached_ebs(session, region)
        if results:
            for ebs in results:
                console.print(f"[red]Volume: {ebs['VolumeId']} | Size: {ebs['Size']}GB | Region: {ebs['Region']}[/red]")
    else:
        console.print("[red] Session fail![/red]")


@scan_app.command("eip")
def scan_eip(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 2: Idle Elastic IPs scan .
    """
    console.print("[cyan] Elastic IP Scan starting.[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        results = scan_unassociated_eip(session, region)
        if results:
            for eip in results:
                console.print(f"[red]IP: {eip['PublicIp']} | ID: {eip['AllocationId']} | Region: {eip['Region']}[/red]")
    else:
        console.print("[red] Session fail![/red]")


@scan_app.command("ec2")
def scan_ec2():
    """
    Day 4-6  implement.
    EC2 instances scan .
    """
    console.print("[yellow] EC2 scanning  added in Day 4-6 .[/yellow]")
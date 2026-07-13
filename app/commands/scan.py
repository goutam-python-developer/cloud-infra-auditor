
"""
scan.py
-------
"""

import typer
from rich.console import Console

scan_app = typer.Typer(help="Scan AWS/GCP resources for waste.")
console = Console()


@scan_app.command("ebs")
def scan_ebs():
    """
    Scan unattached EBS volumes.
    """
    console.print("[yellow]EBS scanning Week 2 add.[/yellow]")


@scan_app.command("eip")
def scan_eip():
    """
    Scan idle Elastic IPs.
    """
    console.print("[yellow] Elastic IP scanning Week 2 add[/yellow]")


@scan_app.command("ec2")
def scan_ec2():
    """ 
    Scan oversized EC2 instances.implemented in week 2
    """
    console.print("[yellow] EC2 scanning Week 2 add .[/yellow]")
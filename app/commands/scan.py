"""
scan.py
-------
Sub-command group for scanning cloud resources.
Actual scanning logic will be implemented in Week 2.

"""

import typer
from rich.console import Console

scan_app = typer.Typer(help="Commands to scan AWS/GCP resources for waste.")
console = Console()


@scan_app.command("ebs")
def scan_ebs():
    """
    (Week 2 me implement hoga) Scan for unattached EBS volumes.
    """
    console.print("[yellow]⚠ EBS scanning logic Week 2 me add hogi.[/yellow]")


@scan_app.command("eip")
def scan_eip():
    """
    (Week 2 me implement hoga) Scan for idle Elastic IPs.
    """
    console.print("[yellow]⚠ Elastic IP scanning logic Week 2 me add hogi.[/yellow]")

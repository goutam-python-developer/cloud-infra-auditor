"""
scan.py
-------
Week 2 - Day 1-3:
EBS aur Elastic IP scan commands
"""

import typer
from rich.console import Console

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





@scan_app.command("all")
def scan_all(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 3: EBS and EIP starting both.
    """
    console.print("[cyan] Full Scan sarting[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        from app.scanner import scan_all_resources
        results = scan_all_resources(session, region)
        console.print(f"[yellow] Total EBS: {len(results['ebs'])}[/yellow]")
        console.print(f"[yellow]Total EIP: {len(results['eip'])}[/yellow]")
    else:
        console.print("[red] Session fail![/red]")    

@scan_app.command("ec2")
def scan_ec2(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """
    Day 4: Underutilized EC2 instances scan .
    """
    console.print("[cyan] EC2 Scan starting.[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        from app.scanner import scan_underutilized_ec2
        results = scan_underutilized_ec2(session, region)
        if results:
            for ec2 in results:
                console.print(
                    f"[red]Instance: {ec2['InstanceId']} | "
                    f"Type: {ec2['InstanceType']} | "
                    f"CPU: {ec2['AvgCPU']}%[/red]"
                )
        else:
            console.print("[green]underutilized EC2 not found![/green]")
    else:
        console.print("[red] Session fail![/red]")

@scan_app.command("ec2-detailed")
def scan_ec2_detailed(
    profile: str = typer.Option("default", help="AWS Profile"),
    region: str = typer.Option("us-east-1", help="AWS Region")
):
    """Day 5: EC2 ka detailed scan starting"""
    console.print("[cyan]EC2 Detailed Scan starting.[/cyan]")
    session = get_aws_session(profile=profile, region=region)
    if session:
        from app.scanner import scan_ec2_detailed
        results = scan_ec2_detailed(session, region)
        if results:
            for ec2 in results:
                status = " Underutilized" if ec2["Underutilized"] else " Normal"
                console.print(
                    f"[cyan]Instance: {ec2['InstanceId']} | "
                    f"Name: {ec2['Name']} | "
                    f"Type: {ec2['InstanceType']} | "
                    f"Avg CPU: {ec2['AvgCPU']}% | "
                    f"Max CPU: {ec2['MaxCPU']}% | "
                    f"{status}[/cyan]"
                )
        else:
            console.print("[green] EC2 not found![/green]")
    else:
        console.print("[red] Session fail![/red]")



@scan_app.command("ec2-regions")
def scan_ec2_regions(
    profile: str = typer.Option("default", help="AWS Profile"),
):
    """Day 6: Multiple regions me EC2 scan """
    console.print("[cyan] Multi-Region EC2 Scan starting[/cyan]")
    session = get_aws_session(profile=profile)
    if session:
        from app.scanner import scan_all_ec2_regions
        results = scan_all_ec2_regions(session)
        for region, instances in results.items():
            console.print(
                f"[yellow]Region: {region} | "
                f"Underutilized: {len(instances)}[/yellow]"
            )
    else:
        console.print("[red] Session fail![/red]")


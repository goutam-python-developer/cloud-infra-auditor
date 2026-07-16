"""
scanner.py
----------
Week 2 - Day 1-3:
EBS volumes and Elastic IPs scan 
"""

from rich.console import Console

console = Console()


def scan_unattached_ebs(session, region: str = "us-east-1"):
    """
    Day 1-2: Unattached EBS volumes .
    """
    console.print(f"[cyan] EBS Volumes scan starting: {region}[/cyan]")

    try:
        ec2 = session.client("ec2", region_name=region)
        response = ec2.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )

        unattached = []
        for volume in response["Volumes"]:
            unattached.append({
                "VolumeId": volume["VolumeId"],
                "Size": volume["Size"],
                "Region": region,
                "State": volume["State"],
                "Type": volume["VolumeType"],
            })

        if unattached:
            console.print(f"[red] {len(unattached)} unattached EBS found![/red]")
        else:
            console.print("[green] NO EBS unattached found![/green]")

        return unattached

    except Exception as e:
        console.print(f"[red] EBS Scan Error: {str(e)}[/red]")
        return []

def scan_all_resources(session, region: str = "us-east-1"):
    """
    Day 3: EBS aur EIP starting both.
    """
    console.print(f"[cyan] Full Scan start: {region}[/cyan]")

    results = {
        "region": region,
        "ebs": [],
        "eip": []
    }

    # EBS scan
    results["ebs"] = scan_unattached_ebs(session, region)

    # EIP scan
    results["eip"] = scan_unassociated_eip(session, region)

    # Summary print 
    console.print(f"[yellow]Scan Complete![/yellow]")
    console.print(f"[red]EBS Issues: {len(results['ebs'])}[/red]")
    console.print(f"[red]EIP Issues: {len(results['eip'])}[/red]")

    return results

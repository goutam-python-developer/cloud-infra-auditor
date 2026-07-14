"""
regions.py
----------
Day 6-7: Cloud regions map
and API rate limits handle 
"""

import time
from rich.console import Console

console = Console()

# AWS ke saare common regions
AWS_REGIONS = [
    "us-east-1",      # N. Virginia
    "us-east-2",      # Ohio
    "us-west-1",      # N. California
    "us-west-2",      # Oregon
    "eu-west-1",      # Ireland
    "eu-central-1",   # Frankfurt
    "ap-south-1",     # Mumbai
    "ap-southeast-1", # Singapore
    "ap-northeast-1", # Tokyo
]


def get_all_regions(session):
    """
    Day 6: AWS regions fetch .
    """
    try:
        ec2 = session.client("ec2", region_name="us-east-1")
        response = ec2.describe_regions()
        regions = [r["RegionName"] for r in response["Regions"]]
        console.print(f"[green] {len(regions)} regions gets![/green]")
        return regions

    except Exception as e:
        console.print(f"[yellow]Default regions are using: {e}[/yellow]")
        return AWS_REGIONS


def safe_api_call(func, delay: float = 0.5, retries: int = 3):
    """
    Day 7: API rate limit handle .
    Automatically retry .
    """
    for attempt in range(retries):
        try:
            result = func()
            time.sleep(delay)
            return result

        except Exception as e:
            if "Throttling" in str(e) or "RequestLimitExceeded" in str(e):
                wait_time = delay * (attempt + 1)
                console.print(f"[yellow]Rate limit! {wait_time}s wait...[/yellow]")
                time.sleep(wait_time)
            else:
                console.print(f"[red] API Error: {str(e)}[/red]")
                return None

    console.print("[red] All retries fail![/red]")
    return None
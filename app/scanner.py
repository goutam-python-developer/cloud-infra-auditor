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


def scan_underutilized_ec2(session, region: str = "us-east-1"):
    """
    Day 4: EC2 instances scan 
    sub-5% CPU using
     check  CloudWatch 
    """
    console.print(f"[cyan] EC2 Instances scan: {region}[/cyan]")

    try:
        ec2 = session.client("ec2", region_name=region)
        cloudwatch = session.client("cloudwatch", region_name=region)

        # Saare running instances lo
        response = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )

        underutilized = []

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]

                # CloudWatch se CPU usage lo
                import datetime
                end_time = datetime.datetime.utcnow()
                start_time = end_time - datetime.timedelta(days=14)

                metrics = cloudwatch.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="CPUUtilization",
                    Dimensions=[
                        {"Name": "InstanceId", "Value": instance_id}
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,
                    Statistics=["Average"]
                )

                # Average CPU calculate karo
                if metrics["Datapoints"]:
                    avg_cpu = sum(
                        d["Average"] for d in metrics["Datapoints"]
                    ) / len(metrics["Datapoints"])
                else:
                    avg_cpu = 0.0

                # Sub 5% CPU wale flag karo
                if avg_cpu < 5.0:
                    underutilized.append({
                        "InstanceId": instance_id,
                        "InstanceType": instance_type,
                        "AvgCPU": round(avg_cpu, 2),
                        "Region": region,
                    })

        if underutilized:
            console.print(f"[red] {len(underutilized)} underutilized EC2 found![/red]")
        else:
            console.print("[green] underutilized EC2 not found![/green]")

        return underutilized

    except Exception as e:
        console.print(f"[red]EC2 Scan Error: {str(e)}[/red]")
        return []



def scan_ec2_detailed(session, region: str = "us-east-1"):
    """
    Day 5: EC2 instances ka detailed scan .
    14 days  CPU data check .
    """
    console.print(f"[cyan]EC2 Detailed Scan: {region}[/cyan]")

    try:
        ec2 = session.client("ec2", region_name=region)
        cloudwatch = session.client("cloudwatch", region_name=region)

        response = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )

        detailed_results = []

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]

                # Instance ka naam lo
                name = "N/A"
                if "Tags" in instance:
                    for tag in instance["Tags"]:
                        if tag["Key"] == "Name":
                            name = tag["Value"]

                import datetime
                end_time = datetime.datetime.utcnow()
                start_time = end_time - datetime.timedelta(days=14)

                # CPU Utilization
                cpu_metrics = cloudwatch.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="CPUUtilization",
                    Dimensions=[
                        {"Name": "InstanceId", "Value": instance_id}
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,
                    Statistics=["Average", "Maximum"]
                )

                avg_cpu = 0.0
                max_cpu = 0.0

                if cpu_metrics["Datapoints"]:
                    avg_cpu = sum(
                        d["Average"] for d in cpu_metrics["Datapoints"]
                    ) / len(cpu_metrics["Datapoints"])
                    max_cpu = max(
                        d["Maximum"] for d in cpu_metrics["Datapoints"]
                    )

                detailed_results.append({
                    "InstanceId": instance_id,
                    "InstanceType": instance_type,
                    "Name": name,
                    "AvgCPU": round(avg_cpu, 2),
                    "MaxCPU": round(max_cpu, 2),
                    "Region": region,
                    "Underutilized": avg_cpu < 5.0
                })

        # Summary print karo
        underutilized_count = sum(
            1 for r in detailed_results if r["Underutilized"]
        )
        console.print(f"[yellow]Total EC2: {len(detailed_results)}[/yellow]")
        console.print(f"[red] Underutilized: {underutilized_count}[/red]")

        return detailed_results

    except Exception as e:
        console.print(f"[red] EC2 Detailed Scan Error: {str(e)}[/red]")
        return []



def scan_all_ec2_regions(session, regions: list = None):
    """
    Day 6: Multiple regions  EC2 scan .
    CloudWatch sub-5% CPU instances finding.
    """
    console.print("[cyan]Multi-Region EC2 Scan starting.[/cyan]")

    if regions is None:
        regions = [
            "us-east-1",
            "us-west-2",
            "eu-west-1",
            "ap-south-1"
        ]

    all_results = {}

    for region in regions:
        console.print(f"[cyan] Region scannig: {region}[/cyan]")
        results = scan_underutilized_ec2(session, region)
        all_results[region] = results

    # Final Summary
    total = sum(len(v) for v in all_results.values())
    console.print(f"[yellow] Total Underutilized EC2: {total}[/yellow]")

    return all_results

def store_scan_results(ebs_results, eip_results, ec2_results, region):
    """
    Day 7: All scan data store Python dictionary structured
    """
    console.print("[cyan]Scan data store starting..[/cyan]")

    scan_data = {
        "metadata": {
            "region": region,
            "total_issues": (
                len(ebs_results) +
                len(eip_results) +
                len(ec2_results)
            ),
            "summary": {
                "unattached_ebs": len(ebs_results),
                "idle_eips": len(eip_results),
                "underutilized_ec2": len(ec2_results),
            }
        },
        "ebs_volumes": ebs_results,
        "elastic_ips": eip_results,
        "ec2_instances": ec2_results,
    }

    # Summary print karo
    console.print("[green] Scan data successfully stored![/green]")
    console.print(
        f"[yellow] Total Issues Found: "
        f"{scan_data['metadata']['total_issues']}[/yellow]"
    )
    console.print(
        f"[red]EBS: {scan_data['metadata']['summary']['unattached_ebs']} | "
        f"EIP: {scan_data['metadata']['summary']['idle_eips']} | "
        f"EC2: {scan_data['metadata']['summary']['underutilized_ec2']}[/red]"
    )

    return scan_data



def generate_report_data(session, region: str = "us-east-1"):
    """
    Day 1: collecting all data for report.
    EBS, EIP and EC2 scanning and store in 
    structured dictionary .
    """
    console.print(f"[cyan]Report data collecting {region}[/cyan]")

    # Saare scans run karo
    ebs = scan_unattached_ebs(session, region)
    eip = scan_unassociated_eip(session, region)
    ec2 = scan_underutilized_ec2(session, region)

    # Data store karo
    report_data = store_scan_results(ebs, eip, ec2, region)

    console.print("[green] Report data ready![/green]")
    return report_data  


def estimate_cost_savings(report_data):
    """
    Day 2: calculate the all resource cost saving .
    """
    console.print("[cyan] Cost savings calculating[/cyan]")

    # Average AWS pricing estimates
    EBS_COST_PER_GB = 0.10      # $0.10 per GB per month
    EIP_COST_PER_IP = 3.60      # $3.60 per idle IP per month
    EC2_COST_PER_INSTANCE = 50  # ~$50 per underutilized instance

    savings = {
        "ebs_savings": 0.0,
        "eip_savings": 0.0,
        "ec2_savings": 0.0,
        "total_savings": 0.0
    }

    # EBS savings
    for ebs in report_data["ebs_volumes"]:
        savings["ebs_savings"] += ebs["Size"] * EBS_COST_PER_GB

    # EIP savings
    savings["eip_savings"] = (
        len(report_data["elastic_ips"]) * EIP_COST_PER_IP
    )

    # EC2 savings
    savings["ec2_savings"] = (
        len(report_data["ec2_instances"]) * EC2_COST_PER_INSTANCE
    )

    # Total savings
    savings["total_savings"] = (
        savings["ebs_savings"] +
        savings["eip_savings"] +
        savings["ec2_savings"]
    )

    console.print(
        f"[green] Total Estimated Savings: "
        f"${savings['total_savings']:.2f}/month[/green]"
    )

    return savings      



def generate_full_report(session, region: str = "us-east-1"):
    """
    Day 3: Complete report generate .
    All  data + cost savings .
    """
    console.print(f"[cyan] Full Report generating: {region}[/cyan]")

    # data All collect 
    report_data = generate_report_data(session, region)

    # Cost savings calculate 
    savings = estimate_cost_savings(report_data)

    # Full report dictionary
    full_report = {
        "metadata": report_data["metadata"],
        "ebs_volumes": report_data["ebs_volumes"],
        "elastic_ips": report_data["elastic_ips"],
        "ec2_instances": report_data["ec2_instances"],
        "cost_savings": savings
    }

    console.print("[green] Full Report Ready![/green]")
    return full_report


def prepare_csv_data(full_report):
    """
    Day 4: Data prepare for CSV export .
    """
    console.print("[cyan] CSV data preparing[/cyan]")

    csv_data = {
        "ebs": [],
        "eip": [],
        "ec2": []
    }

    # EBS data
    for ebs in full_report["ebs_volumes"]:
        csv_data["ebs"].append({
            "Volume ID": ebs["VolumeId"],
            "Size (GB)": ebs["Size"],
            "Type": ebs["Type"],
            "Region": ebs["Region"]
        })

    # EIP data
    for eip in full_report["elastic_ips"]:
        csv_data["eip"].append({
            "Public IP": eip["PublicIp"],
            "Allocation ID": eip["AllocationId"],
            "Region": eip["Region"]
        })

    # EC2 data
    for ec2 in full_report["ec2_instances"]:
        csv_data["ec2"].append({
            "Instance ID": ec2["InstanceId"],
            "Instance Type": ec2["InstanceType"],
            "Avg CPU %": ec2["AvgCPU"],
            "Region": ec2["Region"]
        })

    console.print("[green]CSV data ready![/green]")
    return csv_data



def prepare_json_data(full_report):
    """
    Day 5: Data preparing for JSON export.
    """
    console.print("[cyan] JSON data preparing...[/cyan]")

    import datetime

    json_data = {
        "report_date": datetime.datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "region": full_report["metadata"]["region"],
        "summary": {
            "total_issues": full_report["metadata"]["total_issues"],
            "unattached_ebs": full_report["metadata"]["summary"]["unattached_ebs"],
            "idle_eips": full_report["metadata"]["summary"]["idle_eips"],
            "underutilized_ec2": full_report["metadata"]["summary"]["underutilized_ec2"],
        },
        "cost_savings": {
            "ebs_savings": full_report["cost_savings"]["ebs_savings"],
            "eip_savings": full_report["cost_savings"]["eip_savings"],
            "ec2_savings": full_report["cost_savings"]["ec2_savings"],
            "total_savings": full_report["cost_savings"]["total_savings"],
        },
        "ebs_volumes": full_report["ebs_volumes"],
        "elastic_ips": full_report["elastic_ips"],
        "ec2_instances": full_report["ec2_instances"],
    }

    console.print("[green]JSON data ready![/green]")
    return json_data    
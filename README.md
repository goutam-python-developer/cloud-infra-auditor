# Cloud Infrastructure Auditor & Cost Optimizer (CLI)

A professional-grade CLI tool for DevOps/FinOps teams to scan cloud infra,
find waste, and generate cost-saving reports.

## Week 1 - Day 1-2 Progress
- ✅ CLI framework setup using Typer
- ✅ Command routing structure established (`scan`, `report` sub-command groups)

## Setup

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python -m app.main --help
python -m app.main hello
python -m app.main version
python -m app.main scan ebs
python -m app.main report export
```
## Day 3: Boto3 + Credentials
- Boto3 integrated
- AWS credential handling implemented
-Local AWS profiles support added



### Day 4: Assume Role 
- AWS role assuming functionality add 
- Multiple AWS accounts support

### Day 5: Local AWS Profiles 
- Local machine  AWS profiles list 
- get_local_profiles() function 

### Day 6: Regions Mapping 
- AWS regions map 
- get_all_regions() function 

### Day 7: API Rate Limits 
- API rate limit handler 
- Auto retry logic added
- safe_api_call() function 


## Week 2 Progress 

### Day 1: EBS Scanning 
- scanner.py 
- Unattached EBS volumes scan 

## Day 2: Elastic IP Scanning

- Idle Elastic IPs scan 
- scan.py command added

## Day 3:Full Resource Scan 
- EBS and EIP scanning both
- scan_all_resources() function create
-scan all command added
- scan_all_command also in main.py


### Day 4: EC2 Scanning with CloudWatch 
- EC2 instances scan 
- CPU utilization check through CloudWatch 
- Sub 5% CPU  instances detect 
- scan_underutilized_ec2() function created


### Day 5: EC2 Detailed Scan 
- 14 days CPU data check 
- Average and Maximum CPU fetched
- Instance name and  type detected
- scan_ec2_detailed() function created
- ec2-detailed command added


### Day 6: Multi-Region EC2 Scan 
- EC2 scanning Multiple AWS regions
- every region  stored different result
- scan_all_ec2_regions() function created
- ec2-regions command added

### Day 7: Scan Data Storage 
- All scan data store in  Python dictionaries 
- Structured metadata with region and summary
- EBS, EIP, EC2 results aggregated
- store_scan_results() function created




## Project Structure

cloud-infra-auditor/
├── README.md
├── requirements.txt
└── app/
    ├── main.py
    ├── config.py
    ├── regions.py
    ├── scanner.py
    └── commands/
        ├── scan.py
        └── report.py

## Setup
pip install -r requirements.txt

## Run Commands
### Main Commands
python -m app.main --help
python -m app.main hello
python -m app.main version
python -m app.main connect
python -m app.main profiles
python -m app.main regions
python -m app.main test-api
python -m app.main scan-all
python -m app.main ec2-detailed
python -m app.main ec2-regions
python -m app.main store-all

### scan commands
python -m app.main scan ebs
python -m app.main scan eip
python -m app.main scan all
python -m app.main scan ec2
python -m app.main scan ec2-detailed
python -m app.main scan ec2-regions

### Report commands
python -m app.main report export
python -m app.main report summary

### Day 1-3: Rich Library Reports
### Day 1: Rich Library Tables
- Rich library  beautiful formatted tables creating
- EBS, EIP, EC2  showing in differen  tables 
- Summary table create
- show report command adding
- generate_report_data() function creating

### Day 2: Cost Savings Table 
- Cost savings calculated
- EBS, EIP, EC2 estimated savings
- Showing cost savings in Rich table 
- estimate_cost_savings() function created
- costs command adding
- show-costs command add in  main.py 


### Day 3: Full Report Generator 
-  showing all  report together generate 
- EBS + EIP + EC2 + Cost Savings tables
- generate_full_report() function created
- print_full_report() function created
- full report command adding 
- full-report command added in main.py 

### Day 4: CSV Export 
- Scan results export in  CSV files 
- EBS, EIP, EC2 different  CSV files
- prepare_csv_data() function created
- export_to_csv() function created
- export-csv command adding
- Reports folder automatically created


### Day 5: JSON Export 
- Scan results export in  JSON file 
- Report date and region metadata adding
- Cost savings including in  JSON 
- prepare_json_data() function created
- export_to_json() function created
- export-json command adding
- export-all command adding
- CSV and JSON  exporting both



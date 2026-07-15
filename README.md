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

## Project Structure

cloud-infra-auditor/
├── README.md
├── requirements.txt
└── app/
    ├── main.py
    ├── config.py
    ├── regions.py
    └── commands/
        ├── scan.py
        └── report.py

## Setup
pip install -r requirements.txt

## Run Commands
python -m app.main --help
python -m app.main hello
python -m app.main version
python -m app.main connect
python -m app.main profiles
python -m app.main regions
python -m app.main scan ebs
python -m app.main scan eip
python -m app.main scan ec2
python -m app.main report export
python -m app.main report summary

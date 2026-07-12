"""
config.py
---------
Day 3 :Boto3 integrate  Aws credential handling implement 
"""

import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound
from rich.console import Console


console = Console()


def get_aws_session(profile:str="default",region: str ="us-east-1"):
    

    try:
        session= boto3.Session(
            profile_name=profile,
            region_name=region
        )
        sts=session.client("sts")
        identity=sts.get_caller_identity()
        console.print(f"[green]AWS Connected!Account:{identity['Account']}[/green]")
        return session
    except ProfileNotFound:
        console.print(f"[red] Profile '{profile}' not found![/red]") 
        return None
    except NoCredentialsError:
        console.print("[red] AWS Credentials is not found![/red]")
        return None
    except Exceptionas as e:
        console.print(f"[red] Error : {str(e)}[/red]")           
        return None
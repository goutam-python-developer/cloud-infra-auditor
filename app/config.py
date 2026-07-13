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

def assume_role(session,role_arn:str):
    """
    Day 4: Assume AWS account
    """

    try:
        sts =session.client("sts")
        response= sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName="CloudAuditorSession"
        )
        credentials=response["Credentials"]
        new_session= boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"]
        )
        console.print(f"[green]Role Assume![/green]")
        return new_session
    except Exceptionas as e:
        console.print(f"[red]Role assume failed:{str(e)}[/red]")           
        return None



def get_local_profiles():
    """
    Day 5: Local machine 
    AWS profiles list 
    """
    try:
        session = boto3.Session()
        profiles = session.available_profiles
        console.print(f"[green]Local Profiles found: {profiles}[/green]")
        return profiles

    except Exception as e:
        console.print(f"[red]Profiles not found: {str(e)}[/red]")
        return []
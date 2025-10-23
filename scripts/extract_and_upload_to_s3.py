"""
extract_and_upload_to_s3.py
Fetch JSON data from an API and upload it to an S3 bucket for Snowflake ingestion.
"""

import os
import json
import boto3
import requests
from datetime import datetime
from rich import print

# ---------------- CONFIG ---------------- #
API_URL = os.getenv("API_URL", "https://api.example.com/events")  # Replace
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "my-snowflake-raw-bucket")  # Replace
S3_PREFIX = os.getenv("S3_PREFIX", "api_events/")

# Snowflake metadata (for logs)
SOURCE_NAME = "api_service"
# ---------------------------------------- #


def fetch_api_data():
    """Fetch JSON data from API."""
    print(f"[cyan]Fetching data from API: {API_URL}...[/cyan]")
    response = requests.get(API_URL, timeout=60)
    response.raise_for_status()
    return response.json()


def upload_to_s3(data, s3_client):
    """Upload JSON data to S3 with timestamp-based path."""
    timestamp = datetime.utcnow().strftime("%Y/%m/%d/%H%M%S")
    file_name = f"{S3_PREFIX}api_data_{timestamp}.json"

    print(f"[cyan]Uploading JSON to s3://{S3_BUCKET}/{file_name}...[/cyan]")
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=file_name,
        Body=json.dumps(data),
        ContentType="application/json",
    )
    print("[green]✅ JSON successfully uploaded to S3.[/green]")
    return file_name


def main():
    """Main ETL process."""
    try:
        data = fetch_api_data()
        s3 = boto3.client("s3", region_name=AWS_REGION)
        uploaded_file = upload_to_s3(data, s3)
        print(f"[bold green]✅ Upload complete:[/bold green] {uploaded_file}")
    except Exception as e:
        print(f"[red]❌ ETL failed: {e}[/red]")
        raise


if __name__ == "__main__":
    main()

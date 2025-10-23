"""
extract_and_load_direct.py
Fetch JSON data from an API and insert it directly into Snowflake RAW layer.
"""

import os
import json
import requests
import snowflake.connector
from datetime import datetime
from rich import print

# ---------------- CONFIG ---------------- #
API_URL = os.getenv("API_URL", "https://api.example.com/events")  # Replace
SNOW_ACCOUNT = os.getenv("SNOW_ACCOUNT")
SNOW_USER = os.getenv("SNOW_USER")
SNOW_PWD = os.getenv("SNOW_PWD")
SNOW_ROLE = os.getenv("SNOW_ROLE", "SYSADMIN")
SNOW_WAREHOUSE = os.getenv("SNOW_WAREHOUSE", "COMPUTE_WH")
SNOW_DATABASE = os.getenv("SNOW_DATABASE", "PROJ_E2E_DB")
SNOW_SCHEMA = os.getenv("SNOW_SCHEMA", "RAW")
# ---------------------------------------- #


def fetch_api_data():
    """Fetch data from external API and return as JSON."""
    print(f"[cyan]Fetching data from API: {API_URL}...[/cyan]")
    response = requests.get(API_URL, timeout=60)
    response.raise_for_status()
    return response.json()


def insert_into_snowflake(payload, file_name="api_data"):
    """Insert JSON payload into Snowflake RAW layer."""
    print("[cyan]Connecting to Snowflake...[/cyan]")
    ctx = snowflake.connector.connect(
        user=SNOW_USER,
        password=SNOW_PWD,
        account=SNOW_ACCOUNT,
        role=SNOW_ROLE,
        warehouse=SNOW_WAREHOUSE,
        database=SNOW_DATABASE,
        schema=SNOW_SCHEMA,
    )
    try:
        cs = ctx.cursor()
        insert_sql = """
            INSERT INTO raw.api_events (source_name, file_name, payload)
            VALUES (%s, %s, PARSE_JSON(%s))
        """
        cs.execute(insert_sql, ("api_service", file_name, json.dumps(payload)))
        ctx.commit()
        print("[green]✅ Data successfully inserted into Snowflake RAW layer.[/green]")
    finally:
        cs.close()
        ctx.close()


def main():
    """Main ETL execution."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    try:
        payload = fetch_api_data()
        insert_into_snowflake(payload, file_name=f"api_{timestamp}.json")
    except Exception as e:
        print(f"[red]❌ ETL failed: {e}[/red]")
        raise


if __name__ == "__main__":
    main()

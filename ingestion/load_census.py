import os
import psycopg
from dotenv import load_dotenv
import json
from pathlib import Path
from datetime import datetime, timezone

# Load credentials from .env
load_dotenv()
#retrieves settings from .env file

# Missing-value codes sometimes used in Census estimates
missing_codes = {
    "",
    "-666666666",
    "-222222222",
    "-333333333",
    "-555555555",
    "-999999999",
}

ingestion_time = datetime.now(timezone.utc)

#Find all downloaded census JSON files
files = sorted(Path("data/raw").glob("florida_data*.json"))

if not files:
    print("No census data files found in 'data/raw'. Please run ingestion/census_api.py first.")

#Select the most recent filename
file_path = files[-1]

#Read the JSON data from the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file) 

    print(f"Loaded data from {file_path}. Number of rows (including header): {len(data)}")

headers = data[0]  # First row contains column names
records = data[1:]  # Remaining rows contain the actual data

rows = [dict(zip(headers, record)) for record in records]  # Create a list of dictionaries - makes key value pairs


# Get database connection parameters from environment variables
# os.getenv retrieves particular environment setting
# psycopg.connect establishes a connection to the PostgreSQL database using the provided parameters
with psycopg.connect(
    host = os.getenv("PGHOST"),
    port = os.getenv("PGPORT"),
    dbname = os.getenv("PGDATABASE"),
    user = os.getenv("PGUSER"),
    password = os.getenv("PGPASSWORD")
) as conn:

    print('Successfully connected to the database.')

    #Create a cursor to run SQL commands
    #cur.fetchone() retrieves a single row from the result of the executed query
    with conn.cursor() as cur:
        
        for row in rows:
            rent_value = row["B25058_001E"]

            # Translate unavailable estimates into SQL NULL
            rent = (
                None
                if rent_value in missing_codes
                else int(rent_value)
            )

            cur.execute(
                """
                INSERT INTO raw.census_rent (
                    state_fips,
                    county_fips,
                    county_name,
                    median_contract_rent,
                    dataset_year,
                    ingestion_timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row["state"],
                    row["county"],
                    row["NAME"],
                    rent,
                    2024,
                    ingestion_time
                )
            )

print(f"Loaded {len(rows)} Census records!")






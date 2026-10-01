import os
#read environment settings
import json
#reads and writes json
from pathlib import Path
#works with folders and filenames
from datetime import datetime, timezone
#gets current date and time

import requests
#talks to websites and APIs
from dotenv import load_dotenv
#loads settings from .env file


# Load API credentials form .env file
load_dotenv()
api_key = os.getenv("CENSUS_API_KEY")

if not api_key:
    raise ValueError("CENSUS_API_KEY not found in environment variables. Please set it in your .env file.")

# Census Data from 2024 ACS 5-year dataset
url = "https://api.census.gov/data/2024/acs/acs5"

params = {
    "get": "NAME,B25058_001E",
    "for": "county:*",
    "in": "state:12",
    "key": api_key
}

# Request median contract rent data from the Census API
response = requests.get(url, params=params)
response.raise_for_status()  # Raise an error for bad responses

data = response.json()

#Inspect the data - sample
print("Column Names:", data[0])  # Print column names
print("Sample Data:", data[1])  # Print the first row of data  
print("Number of countries:", len(data) - 1)  # Subtract 1 for the header row

# Save the raw API response
raw_folder = Path("data/raw")
raw_folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't

timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

file_path = raw_folder / f"florida_data{timestamp}.json"

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print('Saved raw data to:', file_path)
import requests
import os
import pandas as pd
from datetime import datetime

def get_eia_api_key():
    return os.environ['eia_api_key']

def test_get_eia_data():
    
    api_key = get_eia_api_key()
    url = "https://api.eia.gov/v2/electricity/rto/region-sub-ba-data/data/"
    params = {
        "frequency": "daily",
        "data[0]": "value",
        "start": "2019-01-01T00",
        "end": "2025-05-31T00",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 5000,
        "api_key": api_key
    }
    r = requests.get(url, params=params)
    grid_data = r.json()
    return grid_data


def save_to_parquet(df, filename):
    """Save a DataFrame to a parquet file in data/parquet/ directory."""
    os.makedirs(os.path.join(os.path.dirname(__file__), '../../data/parquet'), exist_ok=True)
    path = os.path.join(os.path.dirname(__file__), '../../data/parquet', filename)
    df.to_parquet(path, index=False)
    print(f"Saved to {path}")

# Helper for state FIPS or abbreviations
STATE_ABBR = {'CA': 'California', 'TX': 'Texas', 'VA': 'Virginia'}

# Date range for last 7 years
START_DATE = '2018-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')

# SEDS series IDs for key metrics
SEDS_SERIES = {
    'total_consumption': 'TETCB',  # Total Energy Consumption (Btu)
    'total_co2': 'CO2EM',          # Total CO2 Emissions (Metric Tons)
    'electricity_consumption': 'ELETCB',  # Electricity Consumption (Btu)
    'electricity_co2': 'ELCO2',    # Electricity CO2 Emissions (Metric Tons)
}

# State balancing authorities
STATE_BA = {
    'CA': 'CISO',   # California ISO
    'TX': 'ERCO',   # ERCOT (Texas)
    'VA': 'PJM'     # PJM (covers VA and others)
}

# Fetch state level seds data
def fetch_seds_data(api_key, state, series_id):
    url = "https://api.eia.gov/v2/seds/data/"
    params = {
        "frequency": "annual",
        "data[0]": "value",
        "facets[stateId][]": state,
        "facets[seriesId][]": series_id,
        "start": START_DATE[:4],  # SEDS expects year only
        "end": END_DATE[:4],
        "length": 5000,
        "api_key": api_key
    }
    r = requests.get(url, params=params)
    print(f"[DEBUG] SEDS {series_id} {state} status: {r.status_code}")
    print(f"[DEBUG] URL: {r.url}")
    try:
        print(f"[DEBUG] Response: {r.json()}")
    except Exception as e:
        print(f"[DEBUG] Error parsing JSON: {e}")
    return pd.DataFrame(r.json().get('response', {}).get('data', []))

# Function to fetch EIA-930 hourly data for a BA
def fetch_eia930_hourly(api_key, ba_code, start_date, end_date):
    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    all_data = []
    length = 50000  # EIA max per request
    # Move window backwards in time
    window_end = pd.to_datetime(end_date)
    window_size = pd.Timedelta(days=60)  # 2 months per window
    min_date = pd.to_datetime(start_date)
    while window_end > min_date:
        window_start = max(min_date, window_end - window_size)
        offset = 0
        while True:
            params = {
                "frequency": "hourly",
                "data[0]": "value",
                "facets[respondent][]": ba_code,
                "start": window_start.strftime('%Y-%m-%d') + "T00",
                "end": window_end.strftime('%Y-%m-%d') + "T23",
                "length": length,
                "offset": offset,
                "api_key": api_key
            }
            r = requests.get(url, params=params)
            print(f"[DEBUG] EIA-930 {ba_code} status: {r.status_code} offset: {offset} window: {window_start.date()} to {window_end.date()}")
            try:
                data = r.json().get('response', {}).get('data', [])
            except Exception as e:
                print(f"[DEBUG] Error parsing JSON: {e}")
                data = []
            if not data:
                break
            all_data.extend(data)
            if len(data) < length:
                break  # Last page for this window
            offset += length
        window_end = window_start - pd.Timedelta(days=1)
    return pd.DataFrame(all_data)

# Main function to pull and save all SEDS datasets
def pull_and_save_all_seds_data():
    api_key = get_eia_api_key()
    for abbr in STATE_ABBR:
        for key, series_id in SEDS_SERIES.items():
            df = fetch_seds_data(api_key, abbr, series_id)
            save_to_parquet(df, f"seds_{key}_{abbr}.parquet")

# Main function to pull and save EIA-930 hourly data for CA, TX, VA
def pull_and_save_eia930_hourly():
    api_key = get_eia_api_key()
    for abbr, ba_code in STATE_BA.items():
        df = fetch_eia930_hourly(api_key, ba_code, START_DATE, END_DATE)
        save_to_parquet(df, f"eia930_hourly_{abbr}.parquet")

if __name__ == "__main__":
    #pull_and_save_all_seds_data()
    pull_and_save_eia930_hourly()
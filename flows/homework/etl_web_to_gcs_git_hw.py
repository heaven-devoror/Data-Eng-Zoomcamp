from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import pathlib


@task(log_prints=True)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    """Show number of rows in datafile"""
    print(f"Number of rows: {len(df.index)}")

@flow()
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    color = "green"
    year = 2020
    month = 11
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    fetch(dataset_url)


if __name__ == '__main__':
    etl_web_to_gcs()
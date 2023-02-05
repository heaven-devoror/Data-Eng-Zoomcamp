from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task()
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download Trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoomcamp-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write data to bigQuery"""

    gcp_credentials_block = GcpCredentials.load("zoomcamp-gcp-cred")
    df.to_gbq(
        destination_table="dezoomcamp.ny_taxi",
        project_id="dtc-de-course-374912",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"

    )

@flow(log_prints=True)
def etl_web_to_gcs(months: list[int], year: int, color: str) -> None:
    """Main ETL Function"""
    
    for month in months:
        path = extract_from_gcs(color, year, month)
        df = pd.read_parquet(path)
        print(f"Number of rows: {len(df.index)}")
        write_bq(df)

if __name__ == "__main__":
    months = [2,3]
    year = 2019
    color = "yellow"
    etl_web_to_gcs(months, year, color)
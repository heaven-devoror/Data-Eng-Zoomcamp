from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import pathlib
from prefect.filesystems import GitHub


@task()
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """"Write this dataframe to a parquet file"""
    loc = Path.home() / 'Data-Eng-Zoomcamp' / 'week_2_flow' / 'homework' / 'data' / f"{color}"
    try:
        loc.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder is already there")
    else:
        print("Folder was created")
    # path = Path(f"data/{color}/{dataset_file}.parquet")
    file_name = f"{dataset_file}.parquet"
    path = Path(loc / file_name)
    df.to_parquet(path, compression="gzip")
    return path

@task()
def write_gcs(path: Path, color: str, dataset_file: str) -> None:
    """Upload local parquet file to GCS"""
    dest_path = Path(f"data/{color}/{dataset_file}.parquet")
    gcs_block = GcsBucket.load("zoomcamp-bucket")
    gcs_block.upload_from_path(from_path=path, to_path = dest_path)
    return

@task()
github_block = GitHub.load("zoom-repo")


@flow
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    color = "green"
    year = 2020
    month = 11
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    path = write_local(df, color, dataset_file)
    write_gcs(path, color, dataset_file)


if __name__ == '__main__':
    etl_web_to_gcs()
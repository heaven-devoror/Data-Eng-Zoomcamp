from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
# from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception
    df = pd.read_csv(dataset_url, encoding='latin')
    return df

# @task(log_prints=True)
# def clean(df = pd.DataFrame) -> pd.DataFrame:
#     """Fix dtype issues"""
#     # df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
#     # df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
#     df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
#     df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
#     # print(df.head(2))
#     # print(f"columns: {df.dtypes}")
#     # print(f"rows: {len(df)}")
#     return df

# @task()
# def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
#     """"Write this dataframe to a parquet file"""
#     loc = Path.home() / 'Data-Eng-Zoomcamp' / 'week_3_gcp' / 'data' / 'yellow'
#     try:
#         loc.mkdir(parents=True, exist_ok=False)
#     except FileExistsError:
#         print("Folder is already there")
#     else:
#         print("Folder was created")
#     # path = Path(f"data/{color}/{dataset_file}.parquet")
#     file_name = f"{dataset_file}.csv.gz"
#     path = Path(loc / file_name)
#     # df.to_parquet(path, compression='gzip')
#     return path

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """"Write this dataframe to a parquet file"""
    loc = Path.home() / 'Data-Eng-Zoomcamp' / 'week_3_gcp' / 'data' / 'fhv'
    try:
        loc.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder is already there")
    else:
        print("Folder was created")
    # path = Path(f"data/{color}/{dataset_file}.parquet")
    file_name = f"{dataset_file}.csv.gz"
    path = Path(loc / file_name)
    # print(df.dtypes)
    df.to_csv(path, index=False, compression='gzip')
    return path

@task()
def write_gcs(path: Path, dataset_file: str) -> None:
    """Upload local parquet file to GCS"""
    dest_path = Path(f"fhv/{dataset_file}.csv.gz")
    gcs_block = GcsBucket.load("zoomcamp-bucket")
    gcs_block.upload_from_path(from_path=path, to_path=dest_path)
    return


@flow
def etl_web_to_gcs(year: int, month: int) -> None:
    """Main ETL Function"""

    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    # df_clean = clean(df)
    path = write_local(df,dataset_file)
    write_gcs(path, dataset_file)

@flow
def etl_parent_flow(months: int, year: int = 2021):
    for month in range(2,months+1):
        etl_web_to_gcs(year, month)


if __name__ == '__main__':
    # etl_parent_flow(12, 2019)
    etl_parent_flow(12,2020)
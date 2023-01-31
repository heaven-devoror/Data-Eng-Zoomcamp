## Week 2 Workflow Orchestration Homework
> Using google cloud platform VM
> Ubuntu 22.04 LTS

Question 1
> Note: Ignoring DtypeWarning for mixed Columns

<pre><b>touch etl_web_to_gcs.py</b></pre>

```bash
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import pathlib

@task()
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def row_record(df: pd.DataFrame) -> None:
    """Show number of rows in datafile"""
    print(f"Number of rows: {len(df.index)}")


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


@flow
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    color = "green"
    year = 2020
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    row_record(df)
    path = write_local(df, color, dataset_file)
    write_gcs(path, color, dataset_file)

if __name__ == '__main__':
    etl_web_to_gcs()
```
# Copied whole file and updated functions and parameters as required

```bash
python etl_web_to_gcs.py

09:13:12.587 | INFO    | prefect.engine - Created flow run 'marvellous-impala' for flow 'etl-web-to-gcs'
09:13:12.751 | INFO    | Flow run 'marvellous-impala' - Created task run 'fetch-b4598a4a-0' for task 'fetch'
09:13:12.753 | INFO    | Flow run 'marvellous-impala' - Executing 'fetch-b4598a4a-0' immediately...
/home/raviyo123/Data-Eng-Zoomcamp/week_2_flow/homework/etl_web_to_gcs.py:11: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(dataset_url)
09:13:19.310 | INFO    | Task run 'fetch-b4598a4a-0' - Finished in state Completed()
09:13:19.347 | INFO    | Flow run 'marvellous-impala' - Created task run 'row_record-43a666c9-0' for task 'row_record'
09:13:19.349 | INFO    | Flow run 'marvellous-impala' - Executing 'row_record-43a666c9-0' immediately...
09:13:19.404 | INFO    | Task run 'row_record-43a666c9-0' - Number of rows: 447770
09:13:19.438 | INFO    | Task run 'row_record-43a666c9-0' - Finished in state Completed()
09:13:19.472 | INFO    | Flow run 'marvellous-impala' - Created task run 'write_local-f322d1be-0' for task 'write_local'
09:13:19.473 | INFO    | Flow run 'marvellous-impala' - Executing 'write_local-f322d1be-0' immediately...
Folder is already there
09:13:21.206 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
09:13:21.241 | INFO    | Flow run 'marvellous-impala' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
09:13:21.242 | INFO    | Flow run 'marvellous-impala' - Executing 'write_gcs-1145c921-0' immediately...
09:13:21.368 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'prefect-data-storage'.
09:13:22.022 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('/home/raviyo123/Data-Eng-Zoomcamp/week_2_flow/homework/data/green/green_tripdata_2020-01.parquet') to the bucket 'prefect-data-storage' path 'data/green/green_tripdata_2020-01.parquet'.
09:13:22.991 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
09:13:23.032 | INFO    | Flow run 'marvellous-impala' - Finished in state Completed('All states completed.')
```


Answer <pre> 447,770 </pre>

Question 2

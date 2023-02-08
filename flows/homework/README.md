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
```bash
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import pathlib
from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment


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

    cron_dep = Deployment.build_from_flow(
            flow= etl_web_to_gcs,
            name = "cron",
            schedule = (CronSchedule(cron="0 5 1 * *"))
        )
    cron_dep.apply()

    df = fetch(dataset_url)
    row_record(df)
    path = write_local(df, color, dataset_file)
    write_gcs(path, color, dataset_file)


if __name__ == '__main__':
    etl_web_to_gcs()

17:08:30.850 | INFO    | prefect.engine - Created flow run 'refreshing-dugong' for flow 'etl-web-to-gcs'
17:08:31.301 | INFO    | Flow run 'refreshing-dugong' - Created task run 'fetch-b4598a4a-0' for task 'fetch'
17:08:31.304 | INFO    | Flow run 'refreshing-dugong' - Executing 'fetch-b4598a4a-0' immediately...
/home/raviyo123/Data-Eng-Zoomcamp/week_2_flow/homework/etl_web_to_gcs.py:14: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(dataset_url)
17:08:37.283 | INFO    | Task run 'fetch-b4598a4a-0' - Finished in state Completed()
17:08:37.319 | INFO    | Flow run 'refreshing-dugong' - Created task run 'row_record-43a666c9-0' for task 'row_record'
17:08:37.321 | INFO    | Flow run 'refreshing-dugong' - Executing 'row_record-43a666c9-0' immediately...
17:08:37.387 | INFO    | Task run 'row_record-43a666c9-0' - Number of rows: 447770
17:08:37.413 | INFO    | Task run 'row_record-43a666c9-0' - Finished in state Completed()
17:08:37.446 | INFO    | Flow run 'refreshing-dugong' - Created task run 'write_local-f322d1be-0' for task 'write_local'
17:08:37.447 | INFO    | Flow run 'refreshing-dugong' - Executing 'write_local-f322d1be-0' immediately...
Folder is already there
17:08:39.227 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
17:08:39.259 | INFO    | Flow run 'refreshing-dugong' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
17:08:39.260 | INFO    | Flow run 'refreshing-dugong' - Executing 'write_gcs-1145c921-0' immediately...
17:08:39.403 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'prefect-data-storage'.
17:08:40.070 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('/home/raviyo123/Data-Eng-Zoomcamp/week_2_flow/homework/data/green/green_tripdata_2020-01.parquet') to the bucket 'prefect-data-storage' path 'data/green/green_tripdata_2020-01.parquet'.
17:08:41.010 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
17:08:41.050 | INFO    | Flow run 'refreshing-dugong' - Finished in state Completed('All states completed.')
```

<img alt="cron" src="https://i.imgur.com/ki74S4a.jpg">

Answer <pre>0 5 1 * *</pre>

Question 3
<img alt="parquet_data" src="https://i.imgur.com/ZccELbM.jpg">

## We got the data in gcs bucket

```bash
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

19:06:37.713 | INFO    | prefect.engine - Created flow run 'carrot-urchin' for flow 'etl-web-to-gcs'
19:06:37.965 | INFO    | Flow run 'carrot-urchin' - Created task run 'extract_from_gcs-968e3b65-0' for task 'extract_from_gcs'
19:06:37.966 | INFO    | Flow run 'carrot-urchin' - Executing 'extract_from_gcs-968e3b65-0' immediately...
19:06:38.744 | INFO    | Task run 'extract_from_gcs-968e3b65-0' - Downloading blob named data/yellow/yellow_tripdata_2019-02.parquet from the prefect-data-storage bucket to ../data/data/yellow/yellow_tripdata_2019-02.parquet
19:06:42.400 | INFO    | Task run 'extract_from_gcs-968e3b65-0' - Finished in state Completed()
19:06:43.809 | INFO    | Flow run 'carrot-urchin' - Number of rows: 7019375
19:06:43.842 | INFO    | Flow run 'carrot-urchin' - Created task run 'write_bq-b366772c-0' for task 'write_bq'
19:06:43.843 | INFO    | Flow run 'carrot-urchin' - Executing 'write_bq-b366772c-0' immediately...
19:07:49.177 | INFO    | Task run 'write_bq-b366772c-0' - Finished in state Completed()
19:07:49.209 | INFO    | Flow run 'carrot-urchin' - Created task run 'extract_from_gcs-968e3b65-1' for task 'extract_from_gcs'
19:07:49.210 | INFO    | Flow run 'carrot-urchin' - Executing 'extract_from_gcs-968e3b65-1' immediately...
19:07:49.977 | INFO    | Task run 'extract_from_gcs-968e3b65-1' - Downloading blob named data/yellow/yellow_tripdata_2019-03.parquet from the prefect-data-storage bucket to ../data/data/yellow/yellow_tripdata_2019-03.parquet
19:07:53.533 | INFO    | Task run 'extract_from_gcs-968e3b65-1' - Finished in state Completed()
19:07:55.219 | INFO    | Flow run 'carrot-urchin' - Number of rows: 7832545
19:07:55.253 | INFO    | Flow run 'carrot-urchin' - Created task run 'write_bq-b366772c-1' for task 'write_bq'
19:07:55.255 | INFO    | Flow run 'carrot-urchin' - Executing 'write_bq-b366772c-1' immediately...
19:08:49.811 | INFO    | Task run 'write_bq-b366772c-1' - Finished in state Completed()
19:08:49.845 | INFO    | Flow run 'carrot-urchin' - Finished in state Completed('All states completed.')
```
After adding number of rows from both files
<img alt="Number of rows" src="https://i.imgur.com/ygevCBD.jpg">

Answer <pre>14,851,920</pre>

Question 4

# Go to prefect orion server
# Then to blocks
# Add Github block then add your respective repository

<img alt="github block" src="">

# Add etl_web_to_gcs_git_hw.py to github repository

```bash
prefect agent start -q default

prefect deployment build flows/homework/etl_web_to_gcs_git_hw.py:etl_web_to_gcs --name etl_github -sb github/zoom-repo -a
Found flow 'etl-web-to-gcs'
Deployment YAML created at '/home/raviyo123/Data-Eng-Zoomcamp/etl_web_to_gcs-deployment.yaml'.
Deployment storage GitHub(repository='https://github.com/heaven-devoror/Data-Eng-Zoomcamp', reference=None, 
access_token=None) does not have upload capabilities; no files uploaded.  Pass --skip-upload to suppress this 
warning.
Deployment 'etl-web-to-gcs/etl_github' successfully created with id '387f5626-5e55-4346-9744-7718c14a4341'.

prefect deployment run etl-web-to-gcs/etl_github

Agent started! Looking for work from queue(s): default...
17:07:14.357 | INFO    | prefect.agent - Submitting flow run 'd25ea018-4a74-41e8-a137-f295d3fbd2a6'
17:07:14.446 | INFO    | prefect.infrastructure.process - Opening process 'secret-puma'...
17:07:14.477 | INFO    | prefect.agent - Completed submission of flow run 'd25ea018-4a74-41e8-a137-f295d3fbd2a6'
/home/raviyo123/miniconda3/envs/zoom/lib/python3.9/runpy.py:127: RuntimeWarning: 'prefect.engine' found in sys.modules after import of package 'prefect', but prior to execution of 'prefect.engine'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
17:07:17.236 | INFO    | Flow run 'secret-puma' - Downloading flow code from storage at ''
17:07:18.413 | INFO    | Flow run 'secret-puma' - Created task run 'fetch-ba00c645-0' for task 'fetch'
17:07:18.414 | INFO    | Flow run 'secret-puma' - Executing 'fetch-ba00c645-0' immediately...
flows/homework/etl_web_to_gcs_git_hw.py:12: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(dataset_url)
17:07:19.919 | INFO    | Task run 'fetch-ba00c645-0' - Number of rows: 88605
17:07:19.950 | INFO    | Task run 'fetch-ba00c645-0' - Finished in state Completed()
17:07:19.985 | INFO    | Flow run 'secret-puma' - Finished in state Completed('All states completed.')
17:07:20.524 | INFO    | prefect.infrastructure.process - Process 'secret-puma' exited cleanly.
```

Answer <pre>88605</pre>

Question 6

```bash
(base) raviyo123@de-zoomcamp:~/Data-Eng-Zoomcamp$ conda activate zoom
(zoom) raviyo123@de-zoomcamp:~/Data-Eng-Zoomcamp$ prefect orion start

Go to Blocks
Add Secret block
```
<img alt="secret block creation" src="https://i.imgur.com/jggfada.jpg">

<img alt="secret block created" src="https://i.imgur.com/cNlF3mK.jpg">

Answer <pre>8</pre>
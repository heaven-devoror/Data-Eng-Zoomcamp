### Docker HomeWork
> Using git bash command line
> For the ease of reading from command line using | less 

Question 1

```bash
docker build --help | less

      --file string             Name of the Dockerfile (Default is 'PATH/Dockerfile')
      --force-rm                Always remove intermediate containers
      --iidfile string          Write the image ID to the file
      --isolation string        Container isolation technology
      --label list              Set metadata for an image
```

Answer <pre>`--iidfile string     Write the image ID to the file`</pre>

Question 2

```bash
docker run -it --entrypoint=bash python:3.9
```
After excecuting last command
```bash
pip list

Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```

Answer <pre>`3`</pre>

Question 3

Downloading the required file for assesment
```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Open Jupyter notebook
```bash
jupyter notebook
```
Create filename upload_data.ipynb

Import required libraries
```bash
import pandas as pd
from sqlalchemy import create_engine
```

Create connection with localhost with given database
```bash
engine = create_engine('postgresql://root:root@localhost:5430/ny_taxi')
engine.connect()
```

Reading given csv files in two dataframes
```bash
df = pd.read_csv('green_tripdata_2019-01.csv.gz')
df2 = pd.read_csv('taxi+_zone_lookup.csv')
```

changing text columns to datetime format
```bash
df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
```

Creating table
```bash
pd.io.sql.get_schema(df, name='green_taxi_data', con=engine)
pd.io.sql.get_schema(df2, name='green_taxi_location', con=engine)
```

Sending tables data to ny_taxi database 
> Sending data in chunks will be optimal
```bash
df.to_sql(name='green_taxi_data', con=engine, if_exists='replace')
df.to_sql(name='green_taxi_location', con=engine, if_exists='replace')
```

# Checking files in postgres

Connecting to postgres
```bash
pgcli -h localhost -p 5430 -u root -d ny_taxi
```
```bash
root@localhost:ny_taxi> \dt
+--------+---------------------+-------+-------+
| Schema | Name                | Type  | Owner |
|--------+---------------------+-------+-------|
| public | green_taxi_data     | table | root  |
| public | green_taxi_location | table | root  |
+--------+---------------------+-------+-------+
SELECT 2
Time: 0.014s
```
Close the postgres database
ctrl-D OR exit

Create a network to connect to pgAdmin
```bash
docker network create pg-homework
```

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "d:/Data_Eng_Zoomcamp/week_1_setup/docker_sql/ny_taxi_postgres_data":/var/lib/postgresql/data \
  -p 5430:5432 \
  --network=pg-homework \
  --name pg-homebase \
  postgres:13

  PostgreSQL Database directory appears to contain a database; Skipping initialization

2023-01-25 09:42:21.930 UTC [1] LOG:  starting PostgreSQL 13.9 (Debian 13.9-1.pgdg110+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 10.2.1-6) 10.2.1 20210110, 64-bit
2023-01-25 09:42:21.931 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2023-01-25 09:42:21.931 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2023-01-25 09:42:21.984 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2023-01-25 09:42:22.267 UTC [27] LOG:  database system was shut down at 2023-01-25 09:32:55 UTC
2023-01-25 09:42:22.493 UTC [1] LOG:  database system is ready to accept connections
```


```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-homework \
  --name pgadmin-3 \
  dpage/pgadmin4
  
NOTE: Configuring authentication for SERVER mode.

pgAdmin 4 - Application Initialisation
======================================

postfix/postfix-script: starting the Postfix mail system
[2023-01-25 09:43:45 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2023-01-25 09:43:45 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
[2023-01-25 09:43:45 +0000] [1] [INFO] Using worker: gthread
[2023-01-25 09:43:45 +0000] [90] [INFO] Booting worker with pid: 90
  ```

### Querying with posgtgres Admin

Question 3
```bash
SELECT COUNT(1) FROM green_taxi_data
WHERE DATE(lpep_pickup_datetime) = '2019-01-15'
```

Answer `20689`

Question 4
```bash
SELECT date(lpep_pickup_datetime), trip_distance FROM green_taxi_data
ORDER BY trip_distance DESC
LIMIT 1

date              trip_distance
"2019-01-15"	117.99
```

Answer `2019-01-15`


Question 5
```bash
SELECT COUNT(passenger_count) FROM green_taxi_data
WHERE DATE(lpep_pickup_datetime) = '2019-01-01' AND (passenger_count = 2
OR passenger_count = 3)
GROUP BY passenger_count

passenger_count     count
2	              1282
3	              254
```
# Docker and SQL

## Running Postgres with Docker

### Instructions
install all required python libraries from [requirement.txt](https://github.com/heaven-devoror/Data-Eng-Zoomcamp/tree/main/week_1_setup/docker_sql)

> Note: Run Docker desktop before running this code locally
Running postgres on windows git bash

```bash
winpty docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "d:\Data_Eng_Zoomcamp\week_1_setup\docker_sql\ny_taxi_postgres_data":/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```
### Install `pgcli`
```bash
pip install pgcli
```

Using `pgcli` to connect to postgres
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## pdADMIN
Running pgADMIN
```bash
winpty docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

# Running Postgres and pgADMIN together
Create a Network
```bash
docker network create pg-network
```

Running Postgres
```bash
winpty docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "d:\Data_Eng_Zoomcamp\week_1_setup\docker_sql\ny_taxi_postgres_data":/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```
Run pgADMIN
```bash
winpty docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

Data Ingestion
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data2.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```
# Build the image
```bash
docker build -t taxi_ingest:v001 .
```

Running the script with docker
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
# Ingesting Locally
```bash
URL="http://localhost:8000/yellow_tripdata_2021-01.csv"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

# Docker Compose
Run
```bash
docker-compose up
```
Run in detach mode
```bash
docker-compose up -d
```
Shutting Down
```bash
docker-compose down
```
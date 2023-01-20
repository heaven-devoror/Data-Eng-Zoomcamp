# Docker and SQL

## Running Postgres with Docker

### Instructions


> Note: Run Docker desktop before running this code locally
Running postgres on windows git bash

```bash
winpty docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "D:\Data_Eng_Zoomcamp\week_1_setup\docker_sql\ny_taxi_postgres_data":/var/lib/postgresql/data \
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
  -v "D:\Data_Eng_Zoomcamp\week_1_setup\docker_sql\ny_taxi_postgres_data":/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```
Run pgADMIN
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```
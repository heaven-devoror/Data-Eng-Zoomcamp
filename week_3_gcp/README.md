## WEEK 3 Data Warehouse

> Data Present in Bucket

<img alt="data files" src="https://i.imgur.com/H8b6nIy.jpg">

> Create an external table in Bigquery using fhv 2019 data

```bash
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-374912.big_query.external_fhv_data`
OPTIONS (
  format = 'CSV',
  uris = ['gs://prefect-data-storage/fhv_tripdata_2019-*']
);
```

> Create table using external table

```bash
CREATE OR REPLACE TABLE dtc-de-course-374912.big_query.fhv_data_non_partitioned AS
SELECT * FROM dtc-de-course-374912.big_query.external_fahv_data;
```

# Question 1

<img alt="count fhv records" src="https://i.imgur.com/TUzR4bX.jpg">

Answer <pre>43,244,696</pre>

# Question 2

# External table
<img alt="external table" src="https://i.imgur.com/wxfsWhH.jpg">

# Table
<img alt="table" src="https://i.imgur.com/se1zDBA.jpg">

Answer <pre>0 MB for the External Table and 317.94MB for the BQ Table</pre>

# Question 3

<img alt="Null records" src="https://i.imgur.com/EMlkezc.jpg">

Answer <pre>717,748</pre>

# Question 4

Answer <pre>Partition by pickup_datetime Cluster on affiliated_base_number</pre>

# Question 5

# Non Partitioned Table
<img alt="non partitioned" src="https://i.imgur.com/B7Upxvt.jpg">

# Partitioned Table
<img alt="partitioned table" src="https://i.imgur.com/OToo3M2.jpg">

Answer <pre>647.87 MB for non-partitioned table and 23.06 MB for the partitioned table</pre>

# Question 6

Answer <pre>Big Query</pre>

# Question 7

Answer <pre>False</pre>
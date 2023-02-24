## WEEK 4 Analytics Engineering

> Created dbt cloud account and connect it with BigQuery

> DBT REPO - https://github.com/heaven-devoror/dbt

# Question 1
What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)

<img alt='fact trips model' src='https://i.imgur.com/rGZt7ZJ.jpg'>

<img alt='fact_trips_record' src='https://i.imgur.com/OCXpcIn.jpg'>

Answer <pre>61648442</pre>

# Question 2
What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos

<img alt='distribution' src='https://i.imgur.com/B3cHvnP.jpg'>

Answer <pre>89.9/10.1</pre>

# Question 3
What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled (:false)

<img alt='stg_tripdata' src='https://i.imgur.com/nRYP0sk.jpg'>

<img alt='stg_tripdata record' src='https://i.imgur.com/0g5Z44J.jpg'>

Answer <pre>43244696</pre>

# Question 4
What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)

<img alt='fhv_fact_trips' src='https://i.imgur.com/Dj2oZPi.jpg'>

<img alt='fhv_fact_trips_record' src='https://i.imgur.com/vwWQxGl.jpg'>


Answer <pre>22998722</pre>

# Question 5
What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table

<img alt='record trips' src='https://i.imgur.com/1Z4PW5P.jpg'>
<img alt='query run' src='https://i.imgur.com/NxEFWm6.jpg'>

Answer <pre>January</pre>
import pandas as pd
from datetime import timedelta

for month in range(10,12):
    df = pd.read_csv(f'/home/raviyo123/Data-Eng-Zoomcamp/week_3_gcp/data/yellow/yellow_tripdata_2020-{month:02}.csv.gz')
    print(df.dtypes)
    print(' ')
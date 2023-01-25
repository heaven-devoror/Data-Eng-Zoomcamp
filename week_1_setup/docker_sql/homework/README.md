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



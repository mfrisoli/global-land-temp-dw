# LAND TEMPERATURE ETL PIPELINE - DATAWAREHOUSE PROJECT

## Project Summary:

ETL Pipeline - Data Warehouse project to store clean organized data that can be accesable to multiple users on a AWS Redshift cluster

The ETL Pipeline works as described below:

- A Kaggle API is used to get and download the data
- Pandas is used to explore and clean the data
- Dataframe is saved as CSV file and uploaded to AWS s3 bucket
- Data is imported to AWS Redshift
- Data quality tests are carried out to make sure the data exists and is available 

## Files

 - `helpers`: Directory with multiple functions modularized in python scripts.
 - `data`: Directory where the dataset is stored before uploading to s3.
 - `DW.cfg`: Configuration file that has all the main parameters required to create an AWS Redshift cluster using Infrastructure as code (IaC) methodology.
 - `awsUser.cfg`: Configuration with user ID and secret key. File not included in the repository.
 - `Project ETL Notebook.ipynb`: Notebook with ETL pipeline code.
 - `create-redshift-cluster.ipynb`: Notebook used to create AWS Redshift cluster using IaC methodology.
 - `requirements.txt`: File with all python package dependencies created from conda virtual environment.

## Library Requirements

Please refer to `requirements.txt`


## Technologies

- AWS Redshift
- Kaggle API
- AWS s3
- PostgreSQL
- Anaconda3

## Data Model

### Star Schema:

For this project, a Star Schema was selected because of it simple style and its effectiveness to handle simple queries.

![Data Model](media/data_model.png 'Data Model')

#### **Fact Table**
- readings_by_city
    - by_city_id
    - dt
    - city_id
    - avg_temp
    - avg_temp_uncertainty
    - major_city  

#### **Dimension Tables**
- time
    - dt
    - year
    - month
    - day
    - weekday
    - week

- cities
    - city_id
    - country
    - city
    - latitude
    - longitude
    - major_city


### Data Dictionary

Below you will find a summary and example of the schema and data

![Data Dictionary](media/data_dict.JPG 'Data Dictionary')

## How to Run:

### Download Repository to a machine

If you have Git installed you can use the following command to download the repository:

```
$ git clone https://github.com/mfrisoli/global-land-temp-dw.git
``` 

Once the repository is downloaded, create a virtual environment and install the python dependencies. Run the following command, replace `<env>` with your environment name:

```
$ conda create --name <env> --file requirements.txt
```

### Create AWS Redshift Cluster:

Create `awsUser.cfg`: inside the folder use the following command: 

```
$ touch awsUser.cfg
```

Complete `awsUser.cfg` with below information

```
[USER_DETAILS]
KEY=<USER KEY>
SECRET=<USER SECRET KEY>
```

Follow the instruction from `create-redshift-cluster.ipynb` to create the cluster. 

The cluster will be created with the following settings:

- db_name = landtempdb
- db_user = dwhuser
- db_password = Passw0rd
- dwh_port = 5439
- dwh_cluster_type = multi-node
- dwh_num_nodes = 4
- dwh_node_type = dc2.large
- dwh_region = eu-west-1
- dwh_iam_role_name = dwhRole
- dwh_cluster_identifier = dwhCluster
- dwh_db = dwh

Inside the notebook `create-redshift-cluster.ipynb` once you run `prettyRedshiftProps()` and the cluster is available, run the next two blocks to get the cluster Endpoint and role ARN, these will be saved into the `DW.cfg` file. also open the connection to the cluster.

### ETL Pipeline 

Open `Project ETL Notebook.ipynb`.

First thing the notebook will do is to download the raw data from Kaggle using Kaggle API, for this to work you must have access to a Kaggle account.

For more information Kaggle API: https://github.com/Kaggle/kaggle-api

This block of code will download the data to a directory call `~/<Project Directory>/data`.

`kaggle_download('berkeleyearth/climate-change-earth-surface-temperature-data')`

The raw data that we are interested is the following:
- GlobalLandTemperaturesByMajorCity.csv
- GlobalLandTemperaturesByCity.csv

The Notebook will guideyou through data wrangling and the data will be saved locally as a CSV file and then uploaded to AWS s3 bucket of your choice added in the `DW.cgf` file.

Connection will be attempted to the AWS Redshift cluster using `psycopg2`
```
# Connect to redshift database
conn = psycopg2.connect("""host={} 
                           dbname={} 
                           user={} 
                           password={}
                           port={}"""\
                           .format(*config['CLUSTER'].values()
```

The following SQL statments will be run:

Drop Tables if they exist, example below:
```
"DROP TABLE IF EXISTS <table_name>;"
```

Create Tables, example below:

 ```
CREATE TABLE IF NOT EXISTS staging_events (
        index NUMERIC,
        dt DATE NOT NULL,
        AverageTemperature NUMERIC(7,3),
        AverageTemperatureUncertainty NUMERIC(7,3),
        City TEXT,
        Country TEXT,
        Latitude TEXT,
        Longitude TEXT,
        major_city BOOLEAN;
```

Stage data from s3 to Redshift:
```
    COPY staging_events (
        index,
        dt,
        AverageTemperature,
        AverageTemperatureUncertainty,
        City,
        Country,
        Latitude,
        Longitude,
        major_city
    )
    FROM  '{}'
    CREDENTIALS 'aws_iam_role={}'
    REGION '{}'
    DELIMITER ','
    DATEFORMAT 'auto'
    IGNOREHEADER 1;
```

Insert data to Dimension and Fact Tables, example below:

```
    INSERT INTO cities (
        country,
        city,
        latitude,
        longitude,
        major_city
        )
    SELECT DISTINCT country,
        city,
        latitude,
        longitude,
        major_city
    FROM staging_events
    WHERE city IS NOT NULL
    AND city NOT IN (SELECT DISTINCT city FROM cities);
```
## Data Quality Checks:

The data is checked using `data_quality_check()` function from `helpers/data_quality_checks.py` module.

This will check that data exists and is available.

if you get a success message you have succesfully implemented the ETL pipeline and now the Data Warehouse can be used.

## **DISCLAIMER: MAKE SURE THAT ONCE YOU ARE FINISHED USING DW, THE CLUSTER IS DELETED TO AVOID GETTING ADDITIONAL COSTS IN AWS**
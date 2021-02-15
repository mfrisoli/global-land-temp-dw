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
 - `data`: Directory where the dataset is stored befor uploading to s3.
 - `DW.cfg`: Configuration file that has all the main parameters required to create an AWS Redshift cluster using Infrastructure as code (IaC) methodology.
 - `awsUser.cfg`: Configuration with user ID and secret key. File not included in the repository.
 - `Project ETL Notebook.ipynb`: Notebook with ETL pipeline code.
 - `create-redshift-cluster.ipynb`: Notebook used to create AWS Redshift cluster using IaC methodology.
 - `requirements.txt`: File with all python package dependencies.

## Library Requirements

Run the following command to create a conda virtual enviroment and install all python dependencies. replace `<env>` with your envriroment name. 


`$ conda create --name <env> --file requirements.txt`


## Technologies

- AWS Redshift
- Kaggle API
- AWS s3
- PostgreSQL
- Anaconda3

## Data Model

### Star Schema:

The star schema is the simplest style of data mart schema and is the approach most widely used to develop data warehouses and dimensional data marts. The star schema consists of one or more fact tables referencing any number of dimension tables. The star schema is an important special case of the snowflake schema, and is more effective for handling simpler queries <br>
Source: [Wikipedia](https://en.wikipedia.org/wiki/Star_schema)

![Data Model](media/data_model.png 'Data Model')

#### **Fact Table**

#### **Dimension Tables**

## How to Run:

### Download Repository to a machine

You can used the following command if you have git installed to download the repository:

`$ git close https://github.com/mfrisoli/global-land-temp-dw.git`

Run the following command to create a conda virtual enviroment and install all python dependencies. replace `<env>` with your envriroment name. 

`$ conda create --name <env> --file requirements.txt`
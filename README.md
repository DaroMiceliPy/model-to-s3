# Overview

This project consists of an integration between Airflow and LocalStack. Airflow is an orchestrator of data pipelines that allows us to create different DAGs. The DAG of this project contains 6 tasks. The DAG basically downloads GGAL historical data and dollar blue data for Argentina. We merge the data and train a machine learning model, and then we store that machine learning model in an S3 bucket in LocalStack. LocalStack is an emulator of AWS services on a local machine.

![449979633_8070024293035715_8223846438976562042_n (1)](https://github.com/DaroMiceliPy/model-to-s3/assets/66572761/04e164b6-b16f-4e71-a339-e4e7dc61c836)


### Start containers

First, we need to start the containers. In the project folder, execute the following Docker command:

```docker
docker compose up --build
```

### Creating s3 bucket

Next, we need to create the S3 bucket via Terraform. While in the Terraform folder, execute the following:

 ```terraform
terraform init
```

 ```terraform
terraform apply
```

### Setup connection between airflow and localstack

1. From the `Admin > Connections` menu
2. Click the "+"
3. Add an Amazon Web Services connection with the following settings:

    * Connection Id: aws_localstack
    * Login: test
    * Password: test
    * Extra: `{"host": "http://localstack:4566", "region_name": "us-west-1"}`
      
### Run the DAG!

You can run the DAG via Airflow UI or via Airflow CLI.

Airflow CLI:
 ```AIRFLOW
docker compose run airflow-cli dags trigger regression_ggal_blue
```

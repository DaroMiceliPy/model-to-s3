# Overview

This project consists an integration between airflow and localstack. Airflow is a orchestrator of data pipelines, that allow us to create differents DAGs. The DAG of this project contains 6 tasks. The DAG basically
downloa ggal historical data and dollar blue data for Argentina. We merge the data and train a machine learning model, and then, we store that machine learning model to a s3 bucket in localstack. Localstack is a
emulator of AWS services on local machine

![449979633_8070024293035715_8223846438976562042_n (1)](https://github.com/DaroMiceliPy/model-to-s3/assets/66572761/04e164b6-b16f-4e71-a339-e4e7dc61c836)

### Start containers

First we need to up the containers. In the folder of the project we will execute the docker command:

```docker
docker compose up --build
```

### Creating s3 bucket

Later we need to create the s3 bucket via terraform, doing the following being in the terraform folder:

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

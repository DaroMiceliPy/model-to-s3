from airflow.operators.dummy import DummyOperator
from airflow.decorators import task
import pickle
import datetime as dt
import os
import pandas as pd
import requests
from io import StringIO
from sklearn.linear_model import LinearRegression
from airflow.hooks.S3_hook import S3Hook
import yfinance
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="regression_ggal_blue",
    start_date=dt.datetime(2024, 7, 1),
    schedule_interval="0 22 * * *",
    catchup=False
) as dag:

    @task
    def create_folder():
        try:
            os.mkdir("tmp")
            return "/tmp/"
        except FileExistsError:
            print("The folder exists")
            return "/tmp/"

    @task
    def download_ggal(tmp):
        GGAL = yfinance.download('GGAL.BA', start='2011-01-03')
        GGAL = GGAL.reset_index()
        GGAL["Date"] = GGAL["Date"].dt.strftime("%Y-%m-%d")
        GGAL.to_csv(f"{tmp}ggal.csv", index=False)
        
        return f"{tmp}ggal.csv"

    @task
    def download_blue(tmp):
        url = 'https://t.co/W67ufObO5Y'
        response = requests.get(url)
        
        if response.status_code == 200:
            csv_content = StringIO(response.text)
            df = pd.read_csv(csv_content)
            df.to_csv(f"{tmp}blue.csv", index=False)
            return f"{tmp}blue.csv"

    @task
    def join_datasets(path_blue, path_ggal):
        blue_df = pd.read_csv(path_blue)
        ggal_df = pd.read_csv(path_ggal)
        
        blue_df = blue_df[blue_df['type'] == "Blue"]
        blue_df = blue_df.rename(columns={"day": "Date"})
        
        train = ggal_df.merge(blue_df, on="Date")
        train['pct_close'] = train['Close'].pct_change()
        train['pct_blue'] = train['value_sell'].pct_change()
        train = train.dropna(subset=['pct_close'])
        
        train.to_csv("/tmp/train.csv", index=False)
        
        return "/tmp/train.csv"

    @task
    def train_model(path_train):
        train = pd.read_csv(path_train)
        
        model = LinearRegression()
        X = train['pct_blue'].values.reshape(-1, 1)
        Y = train['pct_close'].values
        model.fit(X, Y)

        print(f'Coeficiente (pendiente): {model.coef_[0]}')
        print(f'Intercepto: {model.intercept_}')
        
        with open('/tmp/model.sav', 'wb') as file:
            pickle.dump(model, file)
        return '/tmp/model.sav'
            
    @task
    def upload_to_s3(path_model):
    	hook = S3Hook("aws_localstack")
    	hook.load_file(
    		filename=path_model,
    		key="linear-model/model.sav",
    		bucket_name="ggal-models",
    		replace=True
    	)
    
		
        
    tmp = create_folder()
    path_blue = download_blue(tmp)
    path_ggal = download_ggal(tmp)
    path_train = join_datasets(path_blue, path_ggal)
    path_model = train_model(path_train)
    upload_to_s3(path_model)


   

	


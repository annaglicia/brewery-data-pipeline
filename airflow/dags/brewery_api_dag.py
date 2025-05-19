from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
import json
import pandas as pd

bronze_layer_json_path = '/opt/airflow/db/bronze_layer_data.json'
silver_layer_parquet_path = '/opt/airflow/db/silver_layer_data.parquet'

def read_json(json_path): 
      with open(json_path, 'r') as file:
            data = json.load(file)
            return data
      
def save_raw_data(task_instance):
        data = task_instance.xcom_pull(task_ids=['extract_brewery_data']),
        with open(bronze_layer_json_path, 'w') as f:
                json.dump(data, f)

def first_transformation_data(task_instance):
        data = read_json(bronze_layer_json_path)
        df = pd.DataFrame(data[0][0])
        filtered_df = df.query('country == "United States"')
        filtered_df.to_parquet(path=silver_layer_parquet_path, partition_cols=['city'])
                 
def city_gold_layer_transformation(task_instance):
        df = pd.read_parquet(silver_layer_parquet_path).drop_duplicates()
        
        city_grouped_df = df.groupby(['city', 'brewery_type']).count()
        city_filter_df = city_grouped_df[city_grouped_df["id"] > 0]
        city_final_df = city_filter_df.iloc[:, 0:1].rename(columns={'id': 'count'})
        city_final_df.to_parquet(path='/opt/airflow/db/gold_layer_data/city_type_grouped_data.parquet')

def state_gold_layer_transformation(task_instance):
        df = pd.read_parquet(silver_layer_parquet_path).drop_duplicates()
        
        state_grouped_df = df.groupby(['state_province']).count()
        state_filter_df = state_grouped_df[state_grouped_df["id"] > 0]
        state_final_df = state_filter_df.iloc[:, 0:1].rename(columns={'id': 'count'})
        state_final_df.to_parquet(path='/opt/airflow/db/gold_layer_data/state_grouped_data.parquet')

def type_gold_layer_transformation(task_instance):
        df = pd.read_parquet(silver_layer_parquet_path).drop_duplicates()
        
        type_grouped_df = df.groupby(['brewery_type']).count()
        type_filter_df = type_grouped_df[type_grouped_df["id"] > 0]
        type_final_df = type_filter_df.iloc[:, 0:1].rename(columns={'id': 'count'})
        type_final_df.to_parquet(path='/opt/airflow/db/gold_layer_data/type_grouped_data.parquet')



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

with DAG("brewery_dag",
         default_args=default_args,
         schedule="@daily",
         catchup=False) as dag:
        
        is_api_ready = HttpSensor(
                task_id = 'is_api_ready',
                http_conn_id = 'http_default',
                endpoint = '/v1/breweries'
        )

        extract_brewery_data = HttpOperator(
                task_id = 'extract_brewery_data',
                http_conn_id = 'http_default',
                endpoint = '/v1/breweries',
                method = 'GET',
                response_filter = lambda response: json.loads(response.text),
                log_response = True
        )

        bronze_layer = PythonOperator(
                task_id = 'bronze_layer',
                python_callable = save_raw_data,

        )

        silver_layer = PythonOperator(
                task_id = 'silver_layer',
                python_callable = first_transformation_data,

        )

        gold_layer_city_type = PythonOperator(
               task_id = 'gold_layer_city_type',
               python_callable = city_gold_layer_transformation

        )

        gold_layer_state_type = PythonOperator(
               task_id = 'gold_layer_state_type',
               python_callable = state_gold_layer_transformation

        )

        gold_layer_type = PythonOperator(
               task_id = 'gold_layer_type',
               python_callable = type_gold_layer_transformation

        )

        is_api_ready >> extract_brewery_data >> bronze_layer >> silver_layer >> gold_layer_city_type >> gold_layer_state_type >> gold_layer_type
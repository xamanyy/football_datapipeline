from airflow import DAG
from datetime import datetime


dag = DAG(
    dag_id="football_data",
    default_args={
        "owner":"aman Singh",
        "start_date":datetime(2024,11,14)
    }
)
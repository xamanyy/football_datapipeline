from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import os
import sys

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.extraction_data import main_extract_data,transform_data

dag = DAG(
    dag_id="football_data",
    default_args={
        "owner":"aman Singh",
        "start_date":datetime(2024,11,14)
    },
    schedule_interval=None,
    catchup=False
)

#Extraction

extractData = PythonOperator(
    task_id = "extract_data",
    python_callable= main_extract_data,
    provide_context=True,
    op_kwargs={"url":"https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"},
    dag = dag
)
#Transformation

transformData = PythonOperator(
    task_id = "transform_data",
    provide_context=True,
    python_callable= transform_data,
    dag=dag
)
#Write

extractData >> transformData
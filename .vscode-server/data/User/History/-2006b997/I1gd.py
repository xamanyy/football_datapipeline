from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from pipelines.extaction_data import extractData

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
    python_callable= extractData,
    provide_context=True,
    op_kwargs={
        "url":"https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
    },
    dag = dag
)
#Transformation
#Write
from airflow import DAG
from datetime import datetime


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
    task_id = "python_task",
    python_callable= extractData("https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"),
)
#Transformation
#Write
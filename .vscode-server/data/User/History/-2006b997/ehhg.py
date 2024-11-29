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

extractData = python_task = PythonOperator(
    task_id = "python_task",
    python_callable= ,
    # op_kwargs: Optional[Dict] = None,
)
#Transformation
#Write
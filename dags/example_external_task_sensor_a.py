import time
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


def _executing_task(**kwargs):
    print("Starting task_a")
    time.sleep(200)
    print("Completed task_a")


dag = DAG(
    dag_id="example_external_task_sensor_a",
    default_args={"owner": "airflow"},
    start_date=days_ago(1),
    schedule_interval="*/9 * * * *",
    tags=['example_dags'],
    catchup=False
)
with dag:

    start = DummyOperator(
        task_id='start')

    task_a = PythonOperator(
        task_id='task_a',
        python_callable=_executing_task,
    )

chain(start, task_a)

import time
from airflow import DAG
from airflow.utils.db import provide_session
from airflow.models.dag import get_last_dagrun
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.sensors.external_task import ExternalTaskSensor


def _executing_task():
    time.sleep(30)
    print("Completed task_b")


@provide_session
def _get_execution_date_of_dag_a(exec_date, session=None,  **kwargs):
    dag_a_last_run = get_last_dagrun(
        'example_external_task_sensor_a', session)
    print(dag_a_last_run)
    print(f"EXEC DATE: {dag_a_last_run.execution_date}")
    return dag_a_last_run.execution_date


dag = DAG(
    dag_id="example_external_task_sensor_b",
    default_args={"owner": "airflow"},
    start_date=days_ago(1),
    schedule_interval="*/3 * * * *",
    tags=['example_dags'],
    catchup=False
)
with dag:

    start = DummyOperator(
        task_id='start')

    wait_for_dag_a = ExternalTaskSensor(
        task_id='wait_for_dag_a',
        external_dag_id='example_external_task_sensor_a',
        allowed_states=['success', 'failed'],
        execution_date_fn=_get_execution_date_of_dag_a,
        poke_interval=30
    )
    task_b = PythonOperator(
        task_id='task_b',
        python_callable=_executing_task,
    )

chain(start, wait_for_dag_a,  task_b)

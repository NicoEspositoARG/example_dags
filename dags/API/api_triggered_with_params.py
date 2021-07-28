from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


def _print_params(**kwargs):
    print(f"Task_id: {kwargs['ti'].task_id}")
    for k, v in kwargs["params"].items():
        print(f"{k}:{v}")


dag = DAG(
    dag_id="api_triggered_with_params",
    default_args={"owner": "airflow"},
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["example_dags"],
    params={"param_at_dag_level": "param_66"},
    catchup=False,
)
with dag:

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=_print_params,
    )
    python_task_2 = PythonOperator(
        task_id="python_task_2",
        python_callable=_print_params,
        params={"param4": "param defined at task level"},
    )

chain(python_task, python_task_2)

if __name__ == "__main__":
    from airflow.utils.state import State

    dag.clear(dag_run_state=State.NONE)
    dag.run()

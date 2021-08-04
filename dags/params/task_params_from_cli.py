# see https://stackoverflow.com/a/68659119/10569220
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.models import BaseOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.utils.decorators import apply_defaults


def _get_op(dag):
    PythonOperator(task_id="python_task", python_callable=_print_params, dag=dag)


default_args = {
    "owner": "airflow",
    "params": {"param1": "first_param", "param2": "second_param"},
}


def _print_params(**kwargs):
    print(f"Task_id: {kwargs['ti'].task_id}")
    for k, v in kwargs["params"].items():
        print(f"{k}:{v}")


dag = DAG(
    dag_id="task_params_from_cli",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["example_dags", "params"],
    params={"param_at_dag_level": "param_66"},
    catchup=False,
    doc_md="""Execute from cli with: `airflow tasks test task_params_from_cli
     python_task 20210804 -t '{"param_from_cli":"awesome"}'`""",
)

_get_op(dag)


if __name__ == "__main__":
    from airflow.utils.state import State

    dag.clear(dag_run_state=State.NONE)
    dag.run()

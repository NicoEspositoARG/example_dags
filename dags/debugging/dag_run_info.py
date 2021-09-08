# https://stackoverflow.com/a/69108351/10569220

from airflow import DAG
from airflow.models.dagrun import DagRun
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
}


def _print_dag_run(**kwargs):
    dag_run: DagRun = kwargs["dag_run"]
    print(f"Run type: {dag_run.run_type}")
    print(f"Externally triggered ?: {dag_run.external_trigger}")


dag = DAG(
    dag_id="example_dagRun_info",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["example_dags", "dag_run"],
    catchup=False,
)
with dag:

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=_print_dag_run,
        op_args=["{{ dag_run.run_type }}"],
    )
    bash_task = BashOperator(
        task_id="bash_task",
        bash_command="echo dag_run type is: {{ dag_run.run_type }}",
    )

if __name__ == "__main__":
    from airflow.utils.state import State

    dag.clear(dag_run_state=State.NONE)
    dag.run()

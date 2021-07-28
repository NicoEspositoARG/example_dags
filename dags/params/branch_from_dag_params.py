# see https://stackoverflow.com/a/68477115/10569220

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.python import get_current_context, BranchPythonOperator

default_args = {
    "owner": "airflow",
}

@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["example", "params"],
    params={"enabled": True},
)
def branch_from_dag_params():
    def _print_enabled():
        context = get_current_context()
        enabled = context["params"].get("enabled", False)
        print(f"Task id: {context['ti'].task_id}")
        print(f"Enabled is: {enabled}")

    @task
    def task_a():
        _print_enabled()

    @task
    def task_b():
        _print_enabled()

    def _get_task_run(ti, **kwargs):
        custom_param = kwargs["params"].get("enabled", False)

        if custom_param:
            return "task_a"
        else:
            return "task_b"

    branch_task = BranchPythonOperator(
        task_id="branch_task",
        python_callable=_get_task_run,
    )
    task_a_exec = task_a()
    task_b_exec = task_b()
    branch_task >> [task_a_exec, task_b_exec]


branch_from_dag_params = branch_from_dag_params()

if __name__ == "__main__":
    from airflow.utils.state import State

    branch_from_dag_params.clear(dag_run_state=State.NONE)
    branch_from_dag_params.run()

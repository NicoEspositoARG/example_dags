from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup


NUMS = [1, 2]

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=15),
}


def print_id(num: int):
    print(num)
    return num


def run_tests():
    results = []
    for i in NUMS:
        result = task(task_id=f"run_{i}")(print_id)(i)
        results.append(result)

    return results


@task()
def agg(results):
    print(results)


@dag(
    "test_tg",
    default_args=default_args,
    schedule_interval="@once",
    start_date=days_ago(1),
    max_active_runs=1,
)
def test_supervisor():
    task_start = DummyOperator(task_id="task_start")
    task_end = DummyOperator(task_id="task_end")
    groups = []
    for i in NUMS:
        with TaskGroup(group_id=f"{i}_num_group") as tg:
            results = run_tests()
            aggregation = agg(results)

            groups.append(tg)

    task_start >> groups >> task_end


data_dag = test_supervisor()

if __name__ == "__main__":
    from airflow.utils.state import State

    data_dag.clear(dag_run_state=State.NONE)
    data_dag.run()

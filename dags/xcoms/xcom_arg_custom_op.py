# https://stackoverflow.com/a/67689552/10569220
"""Example DAG demonstrating the usage of XComar_."""
# import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator


class CustomDummyOperator(BaseOperator):
    template_fields = ("msg_from_previous_task",)

    def __init__(self, msg_from_previous_task, *args, **kwargs) -> None:
        super(CustomDummyOperator, self).__init__(*args, **kwargs)
        self.msg_from_previous_task = msg_from_previous_task

    def execute(self, context):
        print(f"Message: {self.msg_from_previous_task}")


dag = DAG(
    "xcom_arg_custom_op",
    schedule_interval="@once",
    start_date=days_ago(2),
    default_args={"owner": "airflow"},
    tags=["example"],
    catchup=False,
)


def return_a_str():
    return "string_value_from_op1"


task_1 = PythonOperator(
    task_id="task_1",
    dag=dag,
    python_callable=return_a_str,
)

task_2 = CustomDummyOperator(
    task_id="task_2", dag=dag,
    msg_from_previous_task=task_1.output
    # msg_from_previous_task="{{ ti.xcom_pull(task_ids='task_1') }}" << equivalent without XcomArgs
)

task_1 >> task_2


if __name__ == "__main__":
    from airflow.utils.state import State

    dag.clear(dag_run_state=State.NONE)
    dag.run()

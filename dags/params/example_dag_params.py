# see https://stackoverflow.com/a/68107775/10569220
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.models import BaseOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


class CustomDummyOperator(BaseOperator):
    def __init__(self, custom_arg: str = "default", *args, **kwargs) -> None:
        self.custom_arg = custom_arg
        super(CustomDummyOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        print(f"Task_id: {self.task_id}")
        print(f"custom_arg: {self.custom_arg}")
        for k, v in context["params"].items():
            print(f"{k}:{v}")


default_args = {
    "owner": "airflow",
    "params": {"param1": "first_param", "param2": "second_param"},
}


def _print_params(**kwargs):
    print(f"Task_id: {kwargs['ti'].task_id}")
    for k, v in kwargs["params"].items():
        print(f"{k}:{v}")


# def outsourced_operator_with_params(params):
#     print(params)
#     return PythonOperator(
#         task_id="task_created_from_func",
#         op_kwargs=params,
#         python_callable=_print_params
#     )


dag = DAG(
    dag_id="example_dag_params",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["example_dags", "params"],
    params={"param_at_dag_level": "param_66"},
    catchup=False,
)
with dag:

    bash_task = BashOperator(
        task_id="bash_task", bash_command="echo bash_task: {{ params.param1 }}"
    )

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=_print_params,
    )
    python_task_2 = PythonOperator(
        task_id="python_task_2",
        python_callable=_print_params,
        params={"param4": "param defined at task level"},
    )
    custom_op_task = CustomDummyOperator(task_id="custom_operator_task")
    # my_params = '{{ execution_date }}'

    # python_task_3 = outsourced_operator_with_params(my_params)

chain(bash_task, python_task, python_task_2, custom_op_task)

if __name__ == "__main__":
    from airflow.utils.state import State

    dag.clear(dag_run_state=State.NONE)
    dag.run()

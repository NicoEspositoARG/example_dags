from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.python import get_current_context

default_args = {
    "owner": "airflow",
}


@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["custom_example", "TaskFlow"],
)
def task_decorator_example():
    def make_request(params):
        print(f"Params: {params}")

    def _print_task_id():
        context = get_current_context()
        print(f"Result: {context['ti'].task_id}")

    @task
    def my_first_function():
        _print_task_id()
        context = get_current_context()
        return make_request(context["params"])

    @task
    def my_second_function():
        _print_task_id()
        params = {"foo": "bar"}
        return make_request(params)

    for i in range(0, 3):
        first = my_first_function()  # this will call "make_request"
        second = my_second_function()  # this will also call "make_request"

        first >> second


example_decorated_dag = task_decorator_example()

if __name__ == "__main__":
    from airflow.utils.state import State

    example_decorated_dag.clear(dag_run_state=State.NONE)
    example_decorated_dag.run()

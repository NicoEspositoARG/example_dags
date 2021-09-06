# https://stackoverflow.com/a/69078440/10569220
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator


def create_dags(city_name, payload: list, default_args):
    """
    Returns a DAG object
    """

    def _print_load_number(city_name, load_number):
        print(f"{load_number} from: {city_name} ")

    dag = DAG(
        f"location_sync_{city_name}",
        schedule_interval="@daily",
        catchup=False,
        tags=["example", "dynamic_dag"],
        default_args=default_args,
    )

    with dag:
        end = DummyOperator(task_id="end")
        for load_no in payload:
            print_load = PythonOperator(
                task_id=f"{city_name}_proccesing_load_{load_no}",
                python_callable=_print_load_number,
                op_kwargs={"city_name": city, "load_number": load_no},
            )
            print_load >> end

    # DAG level tasks dependencies
    return dag


cities = [
    {"name": "London", "payload": [1, 2, 3]},
    {"name": "Paris", "payload": [4, 5, 6]},
    {"name": "Buenos_Aires", "payload": [4, 5, 6]},
]

default_args = {"owner": "Airflow", "start_date": days_ago(1)}

for city in cities:
    dag_id = f"location_sync_{city['name']}"

    globals()[dag_id] = create_dags(city["name"], city["payload"], default_args)

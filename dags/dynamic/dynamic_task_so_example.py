# https://stackoverflow.com/a/66907844/10569220
import json
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup


def _process_obtained_data(ti):
    list_of_cities = ti.xcom_pull(task_ids='get_data')
    Variable.set(key='list_of_cities',
                 value=list_of_cities['cities'], serialize_json=True)


def _print_greeting(city_name, greeting):
    print(f"{greeting} from: {city_name} ")


def _read_file():
    with open('dags/sample_file.json') as f:
        data = json.load(f)
        # push to XCom using return
        return data


with DAG('dynamic_tasks_example', schedule_interval='@once',
         start_date=days_ago(2),
         catchup=False) as dag:

    get_data = PythonOperator(
        task_id='get_data',
        python_callable=_read_file)

    preparation_task = PythonOperator(
        task_id='preparation_task',
        python_callable=_process_obtained_data)

    end = DummyOperator(
        task_id='end',
        trigger_rule='none_failed')

    # Top-level code within DAG block
    iterable_list = Variable.get('list_of_cities',
                                 default_var=['default_city'],
                                 deserialize_json=True)

    with TaskGroup('dynamic_tasks_group',
                   prefix_group_id=False,
                   ) as dynamic_tasks_group:
        if iterable_list:
            for index, city in enumerate(iterable_list):
                say_hello = PythonOperator(
                    task_id=f'say_hello_from_{city}',
                    python_callable=_print_greeting,
                    op_kwargs={'city_name': city, 'greeting': 'Hello'}
                )
                say_goodbye = PythonOperator(
                    task_id=f'say_goodbye_from_{city}',
                    python_callable=_print_greeting,
                    op_kwargs={'city_name': city, 'greeting': 'Goodbye'}
                )

                # TaskGroup level dependencies
                say_hello >> say_goodbye

# DAG level dependencies
get_data >> preparation_task >> dynamic_tasks_group >> end

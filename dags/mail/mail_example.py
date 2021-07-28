

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.email_operator import EmailOperator

default_args = {
    "owner": "airflow",
    'params': {
        "mail_recipients": ["mail1@mail.com", "mail2@mail.com", "mail1@mail.com"]
    }
}


dag = DAG(
    dag_id="mail_example",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=['example_dags'],
    catchup=False
)
with dag:

    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo bash_task: {{ params.mail_recipients }}')

    email_task = EmailOperator(
        to='{{ params.mail_recipients }}',
        task_id='email_task',
        subject='My subject',
        html_content=" Templated HTML content - Today is {{ ds }}"
    )

bash_task >> email_task

if __name__ == '__main__':
    from airflow.utils.state import State
    dag.clear(dag_run_state=State.NONE)
    dag.run()

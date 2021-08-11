# https://stackoverflow.com/a/68749948/10569220
import logging
from airflow.models import DAG
from datetime import timedelta, datetime
from airflow.models.log import Log
from airflow.utils.db import create_session
from airflow.operators.python_operator import PythonOperator


# To test this use this command:
# airflow tasks test killer_dag killer_query {date} -t '{"pid":"pid_value"}'
# Example :
# airflow tasks test killer_dag killer_query 20210803 -t '{"pid":"12345"}'


def kill_query(**kwargs):
    with create_session() as session:
        triggered_by = (
            session.query(Log.dttm, Log.dag_id, Log.execution_date, Log.owner)
            .filter(Log.dag_id == "query_user_triggering_dag", Log.event == "trigger")
            .order_by(Log.dttm.desc())
            .first()[3]
        )
      

    pid = kwargs["params"]["pid"]
    logging.info(f"This PID= '{pid}' is going to be terminated by '{triggered_by}'.")

    killer_query = f"""
        select pg_terminate_backend('{pid}');
    """
    logging.info(killer_query)
    # Making sure the user provides existing pid.
    # In this part the boolean result of terminating select is checked and if False error is raised.
    # analdb_cur.execute(killer_query)
    # result = analdb_cur.fetchone()
    exists = True
    if exists == True:
        logging.info(f"The pid = '{pid}' was terminated by '{triggered_by}'.")
    else:
        logging.info(f"The pid = '{pid}' not found, check it again!")
    return exists


def kill_hanging_queries(killer_dag):
    PythonOperator(
        task_id="kill_query",
        python_callable=kill_query,
        dag=killer_dag,
        # provide_context=True,
    )


killer_dag = DAG(
    dag_id="query_user_triggering_dag",
    default_args={
        "owner": "Data Intelligence: Data Platform",
        "email": "email@mail.com",
        "email_on_failure": True,
        "email_on_retry": False,
        "depends_on_past": False,
        "start_date": datetime(2021, 8, 11, 0, 0, 0),
        "retries": 0,
        "retry_delay": timedelta(minutes=1),
        "params": {"pid": "123"},
    },
)
kill_hanging_queries(killer_dag)


if __name__ == "__main__":
    from airflow.utils.state import State

    killer_dag.clear(dag_run_state=State.NONE)
    killer_dag.run()

# https://stackoverflow.com/a/68869016/10569220
import json
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.utils.db import provide_session
from airflow.models.taskinstance import TaskInstance
from airflow.providers.http.operators.http import SimpleHttpOperator

@dag(
    default_args= {"owner": "airflow"},
    schedule_interval=None,
    start_date=days_ago(0),
    catchup=False,
    tags=["custom_example", "TaskFlow"],
)
def taskflow_previous_task():
    @provide_session
    def _get_upstream_task(upstream_task_id, dag, execution_date, session=None, **_):
        upstream_ti = (
            session.query(TaskInstance)
            .filter(
                TaskInstance.dag_id == dag.dag_id,
                TaskInstance.execution_date == execution_date,
                TaskInstance.task_id == upstream_task_id,
            )
            .first()
        )
        return upstream_ti

    @task
    def job_submission_task(**context):
        print(f"Task Id: {context['ti'].task_id}")

        return {"job_data": "something"}

    @task(trigger_rule='all_done')
    def update_job_status(job_data, **context):
        print(f"Data from previous Task: {job_data['job_data']}")
        upstream_ti = _get_upstream_task("job_submission_task", **context)

        print(f"Upstream_ti state: {upstream_ti.state}")
        return upstream_ti.state

    job_results = job_submission_task()
    job_status = update_job_status(job_results)

    task_post_op = SimpleHttpOperator(
        task_id="post_op",
        endpoint="post",
        data=json.dumps({"job_status": f"{job_status}"}),
        headers={"Content-Type": "application/json"},
        log_response=True,
    )
    job_status >> task_post_op


example_dag = taskflow_previous_task()

if __name__ == "__main__":
    from airflow.utils.state import State

    example_dag.clear(dag_run_state=State.NONE)
    example_dag.run()

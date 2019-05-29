from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

from airflow.operators.python_operator import PythonOperator

from launcher.launcher import launch_docker_container

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 5, 25),
}

pipeline_id = 'pipeline'

with DAG(pipeline_id, default_args=default_args) as dag:

    # EXAMPLE TASK SETUP:
    # t1_id = 'qoa_framework_task_TASK_NAME'
    # t1 = PythonOperator(
    #     task_id=t1_id,
    #     provide_context=True,
    #     op_kwargs={
    #         'image_name': t1_id,
    #         'pipeline_id': pipeline_id
    #     },
    #     python_callable=launch_docker_container
    # )

    # TASK CHAIN:
    # t1 >> 

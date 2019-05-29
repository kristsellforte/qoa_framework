from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

from airflow.operators.python_operator import PythonOperator

from launcher.launcher import launch_docker_container

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 5, 25),
}

pipeline_id = 'qoa_framework_example_pipeline'

with DAG(pipeline_id, default_args=default_args) as dag:

    t1_id = 'qoa_framework_task_clean_data'
    t1 = PythonOperator(
        task_id=t1_id,
        provide_context=True,
        op_kwargs={
            'image_name': t1_id,
            'pipeline_id': pipeline_id
        },
        python_callable=launch_docker_container
    )

    t2_id = 'qoa_framework_task_adjust_data_linear_regression'
    t2 = PythonOperator(
        task_id=t2_id,
        provide_context=True,
        op_kwargs={
            'image_name': t2_id,
            'pipeline_id': pipeline_id
        },
        python_callable=launch_docker_container
    )

    t3_id = 'qoa_framework_task_linear_regression'
    t3 = PythonOperator(
        task_id=t3_id,
        provide_context=True,
        op_kwargs={
            'image_name': t3_id,
            'pipeline_id': pipeline_id
        },
        python_callable=launch_docker_container
    )

    t4_id = 'qoa_framework_task_score_linear_regression'
    t4 = PythonOperator(
        task_id=t4_id,
        provide_context=True,
        op_kwargs={
            'image_name': t4_id,
            'pipeline_id': pipeline_id
        },
        python_callable=launch_docker_container
    )

    t1 >> t2 >> t3 >> t4

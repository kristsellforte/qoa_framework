from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
# from airflow.operators.python_operator import BranchPythonOperator

from launcher.launcher import launch_docker_container

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 6, 9),
}

pipeline_id = 'qoa_framework_example_branching_pipeline'

def do_nothing(**context):
    return True

def decide_after_clean_branch():
    if False:
        return 'qoa_framework_task_filter_data_location'
    else:
        return 'dummy_after_clean'

def decide_after_adjust_branch():
    if False:
        return 'qoa_framework_task_filter_data_date'
    else:
        return 'dummy_after_adjust'

with DAG(pipeline_id, default_args=default_args) as dag:

    # branching related tasks
    branching_after_adjust = BranchPythonOperator(
        task_id='branching_after_adjust',
        python_callable=decide_after_adjust_branch,
        dag=dag,
    )

    branching_after_clean = BranchPythonOperator(
        task_id='branching_after_clean',
        python_callable=decide_after_clean_branch,
        dag=dag,
    )

    join_after_adjust = DummyOperator(
        task_id='join_after_adjust',
        trigger_rule='one_success',
        dag=dag,
    )

    join_after_clean = DummyOperator(
        task_id='join_after_clean',
        trigger_rule='one_success',
        dag=dag,
    )

    dummy_after_adjust = PythonOperator(
        task_id='dummy_after_adjust',
        provide_context=True,
        python_callable=do_nothing,
        dag=dag,
    )

    dummy_after_clean = PythonOperator(
        task_id='dummy_after_clean',
        provide_context=True,
        python_callable=do_nothing,
        dag=dag,
    )

    # actual tasks
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

    t1_1_id = 'qoa_framework_task_filter_data_location'
    t1_1 = PythonOperator(
        task_id=t1_1_id,
        provide_context=True,
        op_kwargs={
            'image_name': t1_1_id,
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

    t2_1_id = 'qoa_framework_task_filter_data_date'
    t2_1 = PythonOperator(
        task_id=t2_1_id,
        provide_context=True,
        op_kwargs={
            'image_name': t2_1_id,
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

    t1 >> branching_after_clean
    branching_after_clean >> t1_1 >> join_after_clean
    branching_after_clean >> dummy_after_clean >> join_after_clean
    join_after_clean >> t2 >> branching_after_adjust
    branching_after_adjust >> t2_1 >> join_after_adjust
    branching_after_adjust >> dummy_after_adjust >> join_after_adjust
    join_after_adjust >> t3 >> t4

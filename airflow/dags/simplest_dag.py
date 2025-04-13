from airflow import DAG
from airflow.operators.bash_operator import BashOperator 

from datetime import datetime,timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

# with DAG(
#     'Hello_ETL',
#     default_args=default_args,
#     description="Senseless ETL DAG",
#     schedule_interval=timedelta(minutes=1),
#     start_date=datetime(2025,3,1),
#     catchup=False
# ) as dag:
dag = DAG(
    'Hello_ETL',
    default_args=default_args,
    description="Senseless ETL DAG",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2025,3,1),
    catchup=False)

run_etl = BashOperator(
    task_id='load_transform_export',
    bash_command='bash /home/parveensharma/Documents/PythonPractice/Airflow_ETL/wrapper.sh ',
    dag=dag
)

run_etl2 = BashOperator(
    task_id='ABC',
    bash_command='bash /home/parveensharma/Documents/PythonPractice/Airflow_ETL/wrapper.sh ',
    dag=dag
)

run_etl >> run_etl2
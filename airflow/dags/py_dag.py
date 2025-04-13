
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

default_args = {
    "owner": "airflow"
}

# TI is task instance, somehow it gets populated on it's own.
def init_name(name,**kwargs):
    print(kwargs.keys)
    ti = kwargs.get('ti')
    # set name in instance variables to access it later. Keep in mind that the max limit for it is 48KB.
    ti.xcom_push(key='name',value=name)
    print(f"The name is ${name}")
    return name
    

def init_age(age,**kwargs):
    ti = kwargs.get('ti')
    name = ti.xcom_pull(task_ids='Get_Name', key='name')
    print(f"The age for ${name} is ${age}")
    return age

def bio(**kwargs):
    ti = kwargs.get('ti')
    name = ti.xcom_pull(task_ids='Get_Name', key='name')
    # No mention of key as this will capture the return value of that task's function.
    age = ti.xcom_pull(task_ids='Get_Age')
    print(f'My name is ${name} and age is ${age}')
    return f'My name is ${name} and age is ${age}'

with DAG(dag_id='PythonOperator_DAG', default_args=default_args, description='Another dag',
    start_date=datetime(2025,3,1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="Get_Name",
        provide_context=True, 
        python_callable=init_name,
        op_kwargs={'name': "Parveen"},
    )

    task2 = PythonOperator(
        task_id='Get_Age',
        provide_context=True, 
        python_callable=init_age,
        op_kwargs={"age": 25}
    )

    task3 = PythonOperator(
        task_id='Get_Bio',
        provide_context=True, 
        python_callable=bio,
    )

    task1 >> task2 >> task3

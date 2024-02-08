from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,2,9,7),
    'retries': 1,
    "catchup":False,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('Termin-Buchung', default_args=default_args, schedule_interval=None)  # Runs every 10 minutes

def task():
    from termin_buchung import sign_up
    sign_up()

t1 = PythonOperator(
    task_id='sign_up',
    python_callable=task,
    dag=dag)

t1
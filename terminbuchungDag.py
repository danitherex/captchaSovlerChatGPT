from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import sys

sys.path.append("/root/airflow/dags/captchaSovlerChatGPT")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,2,9,7,0,0),
    'retries': 1,
    "catchup":False,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('Termin-Buchung', default_args=default_args, schedule_interval ="0 7 * * *") 

t1 = BashOperator(
    task_id='book-termin',
    bash_command='docker-compose up',
    dag=dag,
)
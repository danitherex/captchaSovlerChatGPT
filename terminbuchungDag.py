from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import sys

sys.path.append("/root/airflow/dags/captchaSovlerChatGPT")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,2,11),
    'retries': 2,
    "catchup":False,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('Termin-Buchung', default_args=default_args, schedule_interval ="59 18 * * *") 

t1 = BashOperator(
    task_id='book-termin',
    bash_command='docker run -v $(pwd):/app --env-file /app/.env danitherex/buchungsport',
    dag=dag,
)
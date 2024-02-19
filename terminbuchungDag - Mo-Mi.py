from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import sys

sys.path.append("/root/airflow/dags/captchaSovlerChatGPT")

DISCORD_WEBHOOK = Variable.get("DISCORD_WEBHOOK")
DISCORD_TAG_USER = Variable.get("DISCORD_TAG_USER")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,2,19),
    'retries': 2,
    "catchup":False,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('Termin-Buchung_Mo-Mi', default_args=default_args, schedule_interval ="59 18 * * *") 

def pre_task_code():
    from discord_notifications import send_discord_webhook_notification
    message = "Task has started"
    send_discord_webhook_notification(message,DISCORD_WEBHOOK,DISCORD_TAG_USER)


def post_failure_code(context):
    task_instance = context['task_instance']
    retries = task_instance.max_tries
    current_retry = task_instance.try_number
    # Note: try_number starts at 1, so you may need to adjust the comparison based on your setup
    if current_retry > retries:
        # Your code here
        from discord_notifications import send_discord_webhook_notification
        message = f"Task {context['task_instance'].task_id} has failed after {retries} retries."
        send_discord_webhook_notification(message,DISCORD_WEBHOOK,DISCORD_TAG_USER)

t0 = PythonOperator(
    task_id='pre-task-code',
    python_callable=pre_task_code,
    dag=dag,
)

t1 = BashOperator(
    task_id='book-termin',
    bash_command='docker run --env-file /root/airflow/dags/captchaSovlerChatGPT/.env danitherex/buchungsport',
    dag=dag,
    on_failure_callback=post_failure_code
)

t0 >> t1
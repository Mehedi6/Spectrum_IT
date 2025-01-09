from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os

# Define paths
BASE_DIR = '/home/Ahmed001/airflow/scraper/bd_journal'

# Paths to scripts
LINK_COLLECTOR_SCRIPT = os.path.join(BASE_DIR, 'news_url.py')
DATA_SCRAPER_SCRIPT = os.path.join(BASE_DIR, 'news_data.py')
VALIDATION_SCRIPT = os.path.join(BASE_DIR, 'validation.py')
ARCHIVE_SCRIPT = os.path.join(BASE_DIR, 'archive.py')

# Function to run the link collector script
def run_link_collector():
    print(f"Running link collector: {LINK_COLLECTOR_SCRIPT}")
    result = subprocess.run(['python3', LINK_COLLECTOR_SCRIPT], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running link_collector.py: {result.stderr}")
    print(result.stdout)

# Function to run the data scraper script
def run_data_scraper():
    print(f"Running data scraper: {DATA_SCRAPER_SCRIPT}")
    result = subprocess.run(['python3', DATA_SCRAPER_SCRIPT], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running data_scraper.py: {result.stderr}")
    print(result.stdout)

# Function to run the validation script
def run_validation():
    print(f"Running validation: {VALIDATION_SCRIPT}")
    result = subprocess.run(['python3', VALIDATION_SCRIPT], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running validation.py: {result.stderr}")
    print(result.stdout)

# Function to run the archive script
def run_archive():
    print(f"Running archive: {ARCHIVE_SCRIPT}")
    result = subprocess.run(['python3', ARCHIVE_SCRIPT], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running archive.py: {result.stderr}")
    print(result.stdout)
# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'bdjournal_pipeline',
    default_args=default_args,
    description='Run link collector, data scraper, validation, and archive tasks sequentially',
    schedule_interval='*/60 * * * *',  # Cron expression for every 30 minutes
    start_date=datetime(2024, 12, 29),
    catchup=False,
)

# Define tasks
link_collector_task = PythonOperator(
    task_id='run_link_collector',
    python_callable=run_link_collector,
    dag=dag,
)

data_scraper_task = PythonOperator(
    task_id='run_data_scraper',
    python_callable=run_data_scraper,
    dag=dag,
)

validation_task = PythonOperator(
    task_id='run_validation',
    python_callable=run_validation,
    dag=dag,
)
archive_task = PythonOperator(
    task_id = 'run_archive',
    python_callable = run_archive,
    dag = dag,
)

# Task dependencies
link_collector_task >> data_scraper_task >> validation_task >> archive_task
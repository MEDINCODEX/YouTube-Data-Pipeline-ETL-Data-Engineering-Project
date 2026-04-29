from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Paramètres par défaut du DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 26), # Date de début d'exécution
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1, # Nombre de tentatives en cas d'échec
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG (Tâche planifiée)
dag = DAG(
    'youtube_etl_pipeline_dag',
    default_args=default_args,
    description='Un DAG Airflow pour orchestrer le pipeline ETL YouTube',
    schedule_interval=timedelta(days=1), # Exécution quotidienne
    catchup=False
)

# Définition de la tâche : exécution de notre script principal src/main.py
# Utilisation de BashOperator, méthode la plus simple pour lancer un script Python dans Airflow
run_etl_task = BashOperator(
    task_id='run_python_etl_script',
    bash_command='python /app/src/main.py', # Chemin par défaut si exécuté dans le conteneur Docker d'Airflow
    dag=dag,
)

# Si nous avions plusieurs tâches (ex: extraction -> transformation -> chargement), nous les lierions ainsi :
# extract_task >> transform_task >> load_task

# Puisque tout notre code est centralisé dans main.py, nous n'avons qu'une seule tâche :
run_etl_task
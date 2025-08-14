from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="hello_world_dag",
    start_date=datetime(2025, 8, 13),
    schedule=None,  # Novo nome no Airflow moderno
    catchup=False,
    tags=["example"]
)
def hello_world_pipeline():

    @task
    def say_hello():
        print("Hello World from Airflow with @dag (new syntax)!")

    say_hello()

# Instancia a DAG
hello_world_pipeline()

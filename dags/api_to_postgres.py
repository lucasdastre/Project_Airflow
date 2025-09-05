from include.controller import fetch_pokemon_data,add_pokemon_to_db , gerar_num_aleatorio
from airflow.decorators import dag, task
from datetime import datetime

#O que é um operador?

@dag(
    dag_id="api_postgres",
    description = "api para pegar dados dde pokemon",
    start_date=datetime(2025, 9, 4),
    schedule=None,  # Novo nome no Airflow moderno
    catchup=False,
    tags=["example"]
)
def api_postgres():
    @task(task_id = 'gerar_num_aleatorio')
    def task_gerar_num_aleatorio():
        return gerar_num_aleatorio()
    
    @task(task_id = 'fetch_pokemon_data')
    def task_fetch_pokemon_data(num_ale):
        return fetch_pokemon_data(num_ale)
    

    @task(task_id = 'add_pokemon_to_db')
    def task_add_pokemon_to_db(pokemon_data):
        return add_pokemon_to_db(pokemon_data)
    
    
    t1 = task_gerar_num_aleatorio()
    t2 = task_fetch_pokemon_data(t1)
    t3 = task_add_pokemon_to_db(t2)

    t1 >> t2 >> t3


api_postgres()
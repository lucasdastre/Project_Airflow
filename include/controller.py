import requests
from typing import Optional, Dict, Any
from .db import SessionLocal, engine, Base
from .models import Pokemon
from .schema import PokemonSchema
from random import randint

# Cria as tabelas (ok fazer aqui em dev; em prod, prefira migrações)
Base.metadata.create_all(bind=engine)

def gerar_num_aleatorio() -> int:
    return randint(1, 350)

def fetch_pokemon_data(pokemon_id: int) -> Optional[Dict[str, Any]]:
    try:
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", timeout=10)
        print(resp)
        if resp.status_code != 200:
            return None
        data = resp.json()
        types = ", ".join(t["type"]["name"] for t in data.get("types", []))
        # Em vez de retornar o Schema (objeto), retorne um dict (JSON-serializável)
        schema = PokemonSchema(name=data["name"], type=types)  # valida formato
        return schema.model_dump()  # Pydantic v2
        # Se estiver em Pydantic v1: return schema.dict()
    except requests.RequestException:
        return None

def add_pokemon_to_db(pokemon_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Recebe dict, valida com Pydantic e persiste.
    Retorna um dict simples com os campos gravados.
    """
    if not pokemon_payload:
        return None

    # Garante que o payload está no formato esperado
    schema = PokemonSchema.model_validate(pokemon_payload)

    with SessionLocal() as db:
        db_pokemon = Pokemon(name=schema.name, type=schema.type)
        db.add(db_pokemon)
        db.commit()
        db.refresh(db_pokemon)

        return {
            "id": getattr(db_pokemon, "id", None),
            "name": db_pokemon.name,
            "type": db_pokemon.type,
        }

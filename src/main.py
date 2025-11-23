import uuid
from typing import List, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.models.corrida_model import CorridaIn, CorridaDB
from src.database.mongo_client import get_mongo_collection
from src.database.redis_client import get_redis_client
from src.producer import publish_corrida_finalizada


class CorridaResponse(BaseModel):
    mensagem: str
    id_corrida: str


app = FastAPI(title="TransFlow", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/corridas", response_model=CorridaResponse)
async def criar_corrida(corrida: CorridaIn):
    id_corrida = str(uuid.uuid4())
    corrida_db = CorridaDB(id_corrida=id_corrida, **corrida.dict())
    await publish_corrida_finalizada(corrida_db.dict())
    return CorridaResponse(mensagem="Corrida enviada para processamento.", id_corrida=id_corrida)


@app.get("/corridas", response_model=List[CorridaDB])
def listar_corridas():
    collection = get_mongo_collection()
    docs = list(collection.find({}, {"_id": 0}))
    return docs


@app.get("/corridas/{forma_pagamento}", response_model=List[CorridaDB])
def listar_corridas_por_pagamento(forma_pagamento: str):
    collection = get_mongo_collection()
    docs = list(collection.find({"forma_pagamento": forma_pagamento}, {"_id": 0}))
    return docs


@app.get("/saldo/{motorista}", response_model=Dict[str, float])
def obter_saldo_motorista(motorista: str):
    redis_client = get_redis_client()
    key = f"saldo:{motorista.lower()}"
    saldo = redis_client.get(key)
    if saldo is None:
        raise HTTPException(status_code=404, detail="Saldo não encontrado para esse motorista.")
    return {"motorista": motorista, "saldo": float(saldo)}

from pydantic import BaseModel, Field


class Passageiro(BaseModel):
    nome: str
    telefone: str


class Motorista(BaseModel):
    nome: str
    nota: float


class CorridaIn(BaseModel):
    passageiro: Passageiro
    motorista: Motorista
    origem: str
    destino: str
    valor_corrida: float = Field(gt=0)
    forma_pagamento: str


class CorridaDB(CorridaIn):
    id_corrida: str

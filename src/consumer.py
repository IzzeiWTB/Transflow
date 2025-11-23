import os

from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.database.mongo_client import get_mongo_collection
from src.database.redis_client import get_redis_client

load_dotenv()

rabbit_url = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/")
queue_name = os.getenv("RABBIT_QUEUE", "corrida_finalizada")

broker = RabbitBroker(rabbit_url)
app = FastStream(broker)


@broker.subscriber(queue_name)
async def processar_corrida(msg: dict):
    motorista_nome = msg["motorista"]["nome"].lower()
    valor = float(msg["valor_corrida"])
    redis_client = get_redis_client()
    saldo_key = f"saldo:{motorista_nome}"
    while True:
        pipe = redis_client.pipeline()
        try:
            pipe.watch(saldo_key)
            atual = pipe.get(saldo_key)
            atual_valor = float(atual) if atual else 0.0
            novo_saldo = atual_valor + valor
            pipe.multi()
            pipe.set(saldo_key, novo_saldo)
            pipe.execute()
            break
        except Exception:
            continue
        finally:
            pipe.reset()
    collection = get_mongo_collection()
    collection.update_one({"id_corrida": msg["id_corrida"]}, {"$set": msg}, upsert=True)

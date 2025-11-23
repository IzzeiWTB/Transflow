import json
import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()


async def publish_corrida_finalizada(corrida: dict):
    rabbit_url = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/")
    queue_name = os.getenv("RABBIT_QUEUE", "corrida_finalizada")
    connection = await aio_pika.connect_robust(rabbit_url)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        body = json.dumps(corrida).encode()
        message = aio_pika.Message(
            body=body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(message, routing_key=queue.name)

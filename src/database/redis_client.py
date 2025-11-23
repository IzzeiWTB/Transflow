import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()


def get_redis_client() -> Redis:
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_db = int(os.getenv("REDIS_DB", "0"))
    return Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

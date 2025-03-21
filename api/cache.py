import logging
import os

import redis


def redis_connection():
    return redis.Redis(
    host='redis-15572.c327.europe-west1-2.gce.redns.redis-cloud.com',
    port=15572,
    decode_responses=True,
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
)


def write(redis_client: redis.Redis, original_prompt: str, fixed_prompt: str):
    try:
        redis_client.set(original_prompt, fixed_prompt)
    except Exception as e:
        logging.error("Error saving data to cache:", e)


def read(redis_client: redis.Redis, original_prompt: str) -> None | str:
    try:
        return redis_client.get(original_prompt)
    except Exception:
        return None

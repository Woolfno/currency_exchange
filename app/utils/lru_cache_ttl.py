import functools
import time
from datetime import datetime, timedelta
from functools import lru_cache


def lru_cache_ttl(maxsize=128, typed=False, ttl_delta: timedelta = timedelta(hours=1)):
    def decorator(func):
        cache = dict()

        async def wrapper(*args, **kwargs):
            key = functools._make_key(args, kwargs, typed)

            current_time = time.time()
            if key in cache:
                value, expiration_time = cache[key]
                if current_time < expiration_time:
                    return value
                else:
                    del cache[key]
            result = await func(*args, **kwargs)
            cache[key] = (result, (datetime.now() + ttl_delta).timestamp())
            return result

        return wrapper
    return decorator

import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def set_redis(name, volue, **kwargs):
    redis_client.set(name=name, value=volue, **kwargs)


def get_redis(name):
    try:
        volume = redis_client.get(name).decode('utf-8')

    except:
        volume = False

    return volume

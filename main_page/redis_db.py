import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def set_redis(name, volume):
    redis_client.set(name=name, value=volume)


def get_redis(name):
    volume = redis_client.get(name).decode('utf-8')
    return volume

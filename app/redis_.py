# import redis
#
# from config import REDIS_INFO
#
#
# class RedisExtension(redis.StrictRedis):
#     '''Redis扩展类'''
#     pass
#
#
# pool = redis.ConnectionPool(**REDIS_INFO, decode_responses=True)
# Redis = RedisExtension(connection_pool=pool)

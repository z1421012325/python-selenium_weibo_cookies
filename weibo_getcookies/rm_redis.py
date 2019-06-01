# coding=utf-8

import redis
from weibo_getcookies.redis_config import *

r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB,charset=CHARSET)

count = r.llen(REDIS_KEY_NAME)
for i in range(count):
    r.lpop(REDIS_KEY_NAME)

# print(r.llen(REDIS_KEY_NAME))
print('删除数据,剩余{}'.format(r.llen(REDIS_KEY_NAME)))

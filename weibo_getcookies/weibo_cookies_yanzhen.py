
import redis
import json
import requests
from weibo_getcookies.redis_config import *

r=redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB,charset=CHARSET)

if r.llen(REDIS_KEY_NAME) == 0:
    print('没有数据')
else:
    # 从一个redis中list中pop删除返回一个cookies,再重新加入REDIS_KEY_NAME所在的list中
    a = r.rpoplpush(REDIS_KEY_NAME,REDIS_KEY_NAME)
    cookies = json.loads(a)

    # 进入个人详情页面
    url = 'https://account.weibo.com/set/index?topnav=1&wvr=6'
    headers={
            'Host': 'account.weibo.com',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'cookie':'{}'.format(cookies)
            }

    res = requests.get(url,headers=headers).content.decode()
    print(res)

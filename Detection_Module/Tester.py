from Setting import *
from Storage_Module.RedisDB import RedisClient
import asyncio
import aiohttp
import time
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self,proxy):
        '''
        测试单个代理
        :param proxy:单个代理
        :return: None
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session: #创建独立会话
            try:
                if isinstance(proxy,bytes):    #判断proxy是否为bytes型
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+proxy
                print('正在测试',proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:    #利用代理测试目标网站，超时时间为15s
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)    #将代理分数设置为最大值
                        print('代理可用',proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('响应请求码不合法',proxy)
            except (ClientError,aiohttp.client_exceptions.ClientConnectorError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)      #代理分数-1
                print('代理请求失败', proxy)


    def run(self):
        '''
        测试主函数
        :return: None
        '''
        print('测试器开始执行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            #批量测试 同时测试100个(异步协程)
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误',e.args)


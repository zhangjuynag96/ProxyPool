import redis
from random import choice
from Setting import *
from .Error import PoolEmptyError
'''
    定义RedisClient类，用来操作Redis的有序集合
'''
class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        '''
        初始化
        :param host:地址
        :param port: 端口
        :param password: 密码
        '''
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):
        '''
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        '''
        #如果数据库表不存在，则创建新的数据库表
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        '''
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则异常
        :return: 随机代理
        '''
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE) #对于数据根据分数的从小到大到大，依次排序
        if len(result):
            return choice(result)   #在result列表中随机获取一个代理
        else:
            result = self.db.zrevrange(REDIS_KEY,0,100) #返回成员位置按score值递减来排列（score相同，按字典序的逆序排列）的有序集
            if len(result):
                return choice(result) #在result列表中随机获取一个代理
            else:
                raise PoolEmptyError


    def decrease(self,proxy):
        '''
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        '''
        score = self.db.zscore(REDIS_KEY,proxy) #获取score值
        if score and score > MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY,proxy,-1) #让proxy的score值-1
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)  #移除proxy

    def exists(self,proxy):
        '''
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        '''
        return not self.db.zscore(REDIS_KEY,proxy) == None

    def max(self,proxy):
        '''
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结束
        '''
        print('代理',proxy,'可用，设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)

    def count(self):
        '''
        获取数量
        :return:数量
        '''
        return self.db.zcard(REDIS_KEY) #返回有序集的基数

    def all(self):
        '''
        获取全部代理
        :return: 全部代理列表
        '''
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
'''
    Redis数据库参数
'''
MAX_SCORE = 100 #选取可用代理时初始化的最大分数
MIN_SCORE = 0   #测试代理时的移除代理分数
INITIAL_SCORE = 10 #第一次获取代理时的初始参数
REDIS_HOST =  'localhost' #Redis数据库地址
REDIS_PORT = 6379  #Redis数据库端口
REDIS_PASSWORD = None #Redis数据库密码（有则填，无则None）
REDIS_KEY = 'proxies' #在Redis数据库中所创建的表名

'''
    获取代理模块参数
'''
POOL_UPPER_THRESHOLD = 10000


'''
    检测模块参数
'''
VALID_STATUS_CODES =[200]
TEST_URL = 'http://www.baidu.com' #目的网站地址最佳
BATCH_TEST_SIZE = 100


'''
    调度模块参数
'''
TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True
API_HOST = '0.0.0.0'
API_PORT = 5555
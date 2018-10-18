import redis

#设置配置信息
class Config(object):
    # 调试模式
    DEBUG = True
    SECRET_KEY = "hsdfgfgafv"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@localhost:3306/information16"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600*24*2
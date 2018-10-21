import logging
import redis

#设置配置信息
class Config(object):
    # 调试模式
    DEBUG = True
    SECRET_KEY = "hsdfgfgafv"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@localhost:3306/information16"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True #当链接关闭的时候，会自动提交

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600*24*2 #两天有效期,单位默认就是秒

    # 默认的日志等级
    LEVEL = logging.DEBUG

#开发环境
class DevelopConfig(Config):

    pass

#生产环境(线上环境)
class ProductConfig(Config):
    DEBUG = False
    LEVEL = logging.ERROR

#测试环境
class TestingConfig(Config):
    TESTING = True

#配置环境的统一访问入口
config_dict = {
    "develop":DevelopConfig,
    "product":ProductConfig,
    "testing":TestingConfig
}
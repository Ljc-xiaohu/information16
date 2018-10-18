from flask import Flask,session
from flask_session import Session #指定session存储位置
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect
from config import Config

def create_app():
    app = Flask(__name__)

    # 加载配置类到app
    app.config.from_object(Config)

    # 创建SQLAlchemy对象,关联app
    db = SQLAlchemy(app)

    # 创建redis对象
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

    # 使用CSRFProtect,对app做请求保护
    CSRFProtect(app)

    # 使用Session,关联app,指定存储位置
    Session(app)

    return app
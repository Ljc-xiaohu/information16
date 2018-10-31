import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, session, render_template, g
from flask_session import Session  # 指定session存储位置
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from config import config_dict

# 定义redis_store
from info.utils.commons import index_class, user_login_data

redis_store = None

# 定义db
# db = None
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    # 根据传入的config_name,取出对应的运行环境
    config = config_dict.get(config_name)

    # 调用日志记录方法
    log_file(config.LEVEL)

    # 加载配置类到app
    app.config.from_object(config)

    # 创建SQLAlchemy对象,关联app
    # global db
    # db = SQLAlchemy(app) # 等价于, db = SQLAlchemy(),   db.init_app(app)
    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # 使用CSRFProtect,对app做请求保护
    CSRFProtect(app)

    # 使用Session,关联app,指定存储位置
    Session(app)

    # 将首页蓝图对象index_blue注册到app
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    # 将认证蓝图对象passport_blue注册到app中
    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    # 将新闻蓝图对象news_blue注册到app中
    from info.modules.news import news_blue
    app.register_blueprint(news_blue)

    # 将用户蓝图对象user_blue注册到app中
    from info.modules.user import user_blue
    app.register_blueprint(user_blue)

    # 将过滤器,添加到默认过滤器列表中
    app.add_template_filter(index_class, "index_class")

    # 捕捉404错误信息
    @app.errorhandler(404)
    @user_login_data
    def page_not_found(e):
        data = {"user_info": g.user.to_dict() if g.user else ""}
        return render_template("news/404.html", data=data)

    # 使用请求钩子,after_request拦截所有响应
    @app.after_request
    def after_request(resp):
        value = generate_csrf()
        resp.set_cookie("csrf_token", value)
        return resp

    print(app.url_map)
    return app


# 日志记录方法
def log_file(LEVEL):
    # 设置日志的记录等级, 常见的日志有: DEBUG < INFO < WARING < ERROR
    logging.basicConfig(level=LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

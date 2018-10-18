"""
项目的初始化配置信息:
项目的初始化配置信息:

1.数据库配置

2.redis配置

3.csrf配置,对'POST', 'PUT', 'PATCH', 'DELETE'请求方式做保护

4.session配置,为了后续登陆保持,做铺垫

5.日志信息配置

6.数据库迁移配置

"""""
import logging
from flask import current_app
from info import create_app

#调用业务模块获取app
app = create_app("product")


@app.route('/')
def hello_world():

    # redis_store.set("name","laowang")
    # print(redis_store.get("name"))
    #
    # session["age"] = "13"
    # print(session.get("age"))

    logging.debug("调试信息1")
    logging.info("详细信息1")
    logging.warning("警告信息1")
    logging.error("错误信息1")

    # current_app.logger.debug("调试信息2")
    # current_app.logger.info("详细信息2")
    # current_app.logger.warning("警告信息2")
    # current_app.logger.error("错误信息2")

    return "helloworld100"

if __name__ == '__main__':
    app.run()
from flask import session

from info import redis_store
from info.models import User
from . import index_blu
from flask import render_template,current_app




@index_blu.route('/')
def hello_world():

    # 1.取出session,中的用户编号
    user_id = session.get("user_id")

    # 2.获取用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 3.拼接用户数据渲染页面
    data = {
        # 如果user不为空,返回左边的内容, 为空返回右边内容
        "user_info":user.to_dict() if user else ""
    }

    return render_template("news/index.html",data=data)

#处理网站logo
#每个浏览器在访问服务器的时候,会自动向该服务器发送GET请求,地址是:/favicon.ico
#获取静态文件夹资源: current_app.send_static_file("文件路径"),会自动寻找static静态文件夹的资源
@index_blu.route('/favicon.ico')
def web_logo():

    return current_app.send_static_file("news/favicon.ico")
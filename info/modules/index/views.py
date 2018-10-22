from flask import session, jsonify

from info import redis_store
from info.models import User, News, Category
from info.utils.response_code import RET
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

    # 2.1 热门新闻,按照新闻的点击量量,查询前十条新闻
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取新闻失败")

    # 2.2 将新闻列表对象,字典列表对象
    click_news_list = []
    for news in news_list:
        click_news_list.append(news.to_dict())

    # 2.3 查询所有分类信息
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)

    # 2.4 将分类对象列表,转成字典列表
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    # 3.拼接用户数据渲染页面
    data = {
        # 如果user不为空,返回左边的内容, 为空返回右边内容
        "user_info":user.to_dict() if user else "",
        "click_news_list":click_news_list,
        "categories":category_list
    }

    return render_template("news/index.html",data=data)

#处理网站logo
#每个浏览器在访问服务器的时候,会自动向该服务器发送GET请求,地址是:/favicon.ico
#获取静态文件夹资源: current_app.send_static_file("文件路径"),会自动寻找static静态文件夹的资源
@index_blu.route('/favicon.ico')
def web_logo():

    return current_app.send_static_file("news/favicon.ico")
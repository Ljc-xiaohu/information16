from info.models import News, User
from info.utils.commons import user_login_data
from info.utils.response_code import RET
from . import news_blue
from flask import render_template,current_app, jsonify,abort,session,g

# 获取新闻详情
# 请求路径: /news/<int:news_id>
# 请求方式: GET
# 请求参数:news_id
# 返回值: detail.html页面, 用户data字典数据
@news_blue.route('/<int:news_id>')
@user_login_data
def news_blue(news_id):

    # 1.根据新闻编号获取,新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="新闻获取失败")

    # 2.判断新闻对象是否存在,后续会对404做统一处理
    if not news:
        abort(404)

    # 2.1 热门新闻,按照新闻的点击量量,查询前十条新闻
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(8).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取新闻失败")

    # 2.2 将新闻列表对象,字典列表对象
    # click_news 不要与上面的news 重名，不然会覆盖原来的名字
    click_news_list = []
    for click_news in news_list:
        click_news_list.append(click_news.to_dict())

    # 2.3 判断用户是否收藏了该新闻
    is_collected = False
    if g.user and news in g.user.collection_news:
        is_collected = True


    # 3.携带新闻数据,到模板页面显示
    data = {
        "news":news.to_dict(),
        "click_news_list":click_news_list,
        "user_info": g.user.to_dict() if g.user else "",
        "is_collected":is_collected
    }

    return render_template("news/detail.html",data=data)
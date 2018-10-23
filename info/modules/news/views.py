from info import db
from info.models import News, User, Comment
from info.utils.commons import user_login_data
from info.utils.response_code import RET
from . import news_blue
from flask import render_template, current_app, jsonify, abort, session, g, request


# 功能描述: 评论
# 请求路径: /news/news_comment
# 请求方式: POST
# 请求参数:news_id,comment,parent_id, g.user
# 返回值: errno,errmsg,评论字典
@news_blue.route('/news_comment', methods=['POST'])
@user_login_data
def news_comment():
    """
    - 1.判断用户是否登陆
    - 2.获取参数
    - 3.校验参数,为空检验
    - 4.根据新闻编号取出新闻对象
    - 5.判断新闻对象是否存在
    - 6.创建评论对象,设置属性
    - 7.保存评论到数据库
    - 8.返回响应
    :return:
    """
    # - 1.判断用户是否登陆
    if not g.user:
        return jsonify(errno=RET.NODATA, errmsg="用户未登录")

    # - 2.获取参数
    news_id = request.json.get("news_id")
    content = request.json.get("comment")
    parent_id = request.json.get("parent_id")

    # - 3.校验参数,为空检验
    if not all([news_id, content, parent_id]):
        jsonify(errno=RET.NODATA, errmsg="参数不全")

    # - 4.根据新闻编号取出新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    # - 5.判断新闻对象是否存在
    if not news: return jsonify(errno=RET.NODATA, errmsg="新闻不存在")

    # - 6.创建评论对象,设置属性
    comment = Comment()
    comment.user_id = g.user.id
    comment.news_id = news_id
    comment.content = content
    if parent_id:
        comment.parent_id = parent_id

    # - 7.保存评论到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="评论失败")

    # - 8.返回响应
    return jsonify(errno=RET.OK, errmsg="评论成功")


# 功能描述: 收藏取消收藏
# 请求路径: /news/news_collect
# 请求方式: POST
# 请求参数:news_id,action, g.user
# 返回值: errno,errmsg
@news_blue.route('/news_collect', methods=['POST'])
@user_login_data
def news_collect():
    """
    1. 判断用户登陆状态
    2. 获取参数
    3. 校验参数,为空校验
    4. 判断操作类型
    5. 通过新闻编号取出新闻对象
    6. 判断新闻对象是否存在
    7. 根据操作类型,收藏,取消操作
    8. 返回响应
    :return:
    """

    # 1. 判断用户登陆状态
    if not g.user:
        return jsonify(errno=RET.NODATA, errmsg="用户未登录")

    # 2. 获取参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")

    # 3. 校验参数,为空校验
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 4. 判断操作类型
    if not action in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.DATAERR, errmsg="操作类型有误")

    # 5. 通过新闻编号取出新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="新闻获取失败")

    # 6. 判断新闻对象是否存在
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="新闻不存在")
    try:
        # 7. 根据操作类型,收藏,取消操作
        if action == "collect":
            # 判断用户是否已经对该新闻收藏了
            if not news in g.user.collection_news:
                g.user.collection_news.append(news)
        else:
            # 判断用户是否已经对该新闻收藏了
            if news in g.user.collection_news:
                g.user.collection_news.remove(news)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败")

    # 8. 返回响应
    return jsonify(errno=RET.OK, errmsg="操作成功")


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
        return jsonify(errno=RET.DBERR, errmsg="新闻获取失败")

    # 2.判断新闻对象是否存在,后续会对404做统一处理
    if not news:
        abort(404)

    # 2.1 热门新闻,按照新闻的点击量量,查询前十条新闻
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(8).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

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
        "news": news.to_dict(),
        "click_news_list": click_news_list,
        "user_info": g.user.to_dict() if g.user else "",
        "is_collected": is_collected
    }

    return render_template("news/detail.html", data=data)

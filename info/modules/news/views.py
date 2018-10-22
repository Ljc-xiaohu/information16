from info.models import News
from info.utils.response_code import RET
from . import news_blue
from flask import render_template,current_app, jsonify,abort

# 获取新闻详情
# 请求路径: /news/<int:news_id>
# 请求方式: GET
# 请求参数:news_id
# 返回值: detail.html页面, 用户data字典数据
@news_blue.route('/<int:news_id>')
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

    # 3.携带新闻数据,到模板页面显示
    data = {
        "news":news.to_dict()
    }

    return render_template("news/detail.html",data=data)
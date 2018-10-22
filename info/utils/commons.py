#定义公共代码,过滤器

#自定义过滤器,实现颜色过滤
from flask import session,current_app,g


def index_class(index):
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    else:
        return ""

#用户登陆的装饰器
def user_login_data(view_func):
    def wrapper(*args,**kwargs):

        # 取出sessioin,用户编号
        user_id = session.get("user_id")

        # 获取用户对象
        user = None
        if user_id:
            try:
                from info.models import User
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)

        # 将user添加到g对象中
        g.user = user

        return view_func(*args,**kwargs)
    return wrapper
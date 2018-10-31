from flask import Blueprint, request, session, redirect

# 创建管理员蓝图对象
admin_blue = Blueprint("admin", __name__, url_prefix="/admin")

# 装饰视图函数
from . import views


@admin_blue.before_request
def visit_admin():
    # 拦截普通用户访问, 管理员的非登录页面
    # 管理员用户,不需要拦截
    # if request.url.endswith("/admin/login"):
    #     pass
    # else:
    #     #判断是,管理员还是普通用户
    #     if session.get("is_admin"):
    #         pass
    #     else:
    #         return redirect("/")
    # 优化一下
    if not request.url.endswith("/admin/login"):
        if not session.get("is_admin"):
            return redirect("/")

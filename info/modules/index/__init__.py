from flask import Blueprint

#创建蓝图对象
index_blu = Blueprint("index",__name__)

#装饰视图函数
# from info.modules.index import views
from . import views
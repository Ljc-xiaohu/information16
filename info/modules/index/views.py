from info.models import User, News, Category
from info.utils.commons import user_login_data
from info.utils.response_code import RET
from . import index_blu
from flask import render_template,current_app,session,jsonify,request,g

#功能描述: 首页新闻列表获取
# 请求路径: /newslist
# 请求方式: GET
# 请求参数: cid,page,per_page
# 返回值: data数据
@index_blu.route('/newslist')
def news_list():
    """
    1.获取参数
    2.参数类型转换,为了分页 做准备,paginate(page,per_page,False)
    3.分页查询
    4.取出分页对象中的属性,总页数,当前页,当前页对象
    5.将当前页对象列表,转成字典列表
    6.返回响应
    :return:
    """
    # 1.获取参数
    cid = request.args.get("cid","1")
    page = request.args.get("page","1")
    per_page = request.args.get("per_page","10")

    # 2.参数类型转换,为了分页 做准备,paginate(page,per_page,False)
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        page = 1
        per_page = 10

    # 3.分页查询
    #     下面代码等价,一个没换行，一个换行了,太长了,在.后面敲Enter键便得到\
    #     paginate = News.query.filter(News.category_id == cid).order_by(News.create_time.desc()).paginate(page, per_page, False)

        # paginate = News.query.filter(News.category_id == cid).order_by(News.create_time.desc()).paginate(page, per_page,
        #                                                                                                  False)
    # 第一种写法
        # 判断是否cid != 1, 不是最新
        # condition = ""
        # if cid != "1":
        #     condition = (News.category_id == cid)
        # paginate = News.query.filter(condition).\
        #     order_by(News.create_time.desc()).\
        #     paginate(page,per_page,False)

        # 判断是否cid != 1, 不是最新
    """
    # 第二种写法（推荐）
    """
    # 拆包，例如filters = [1,2]
    # a,b = *filters
    # 结果便是a=1,b=2
    # 这样写的好处是 ：可以加多个条件
    # if cid != "1":
    #     filters.append(News.category_id == cid)
    # if cid != "2":
    #     filters.append(News.category_id == cid)
    """
    其中的News.category_id == cid，表示一个结果集或者对象，
    一般来说，a==b是True和False，而News.category_id == cid不是，
    原因在于object基类中的__eq__方法没有被重写
    举例如下：
    In [10]: class Person(object):
    ...:     pass
    ...:
    In [11]: p1 = Person()
    In [12]: p2 = Person()
    In [13]: p1 == p2
    Out[13]: False
    In [14]: class Student(object):
        ...:     def __eq__(self,obj):
        ...:         return "hahaha"
        ...:
    In [15]: s1 = Student()
    In [16]: s2 = Student()
    In [17]: s1 == s2
    Out[17]: 'hahaha'
    """

    try:
        filters = []
        if cid != "1":
            filters.append(News.category_id == cid)
        paginate = News.query.filter(*filters).\
            order_by(News.create_time.desc()).\
            paginate(page,per_page,False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取新闻失败")

    # 4.取出分页对象中的属性,总页数,当前页,当前页对象
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5.将当前页对象列表,转成字典列表
    newsList = []
    for item in items:
        newsList.append(item.to_dict())

    # 6.返回响应
    return jsonify(errno=RET.OK,errmsg="获取成功",totalPage=totalPage,currentPage=currentPage,newsList=newsList)


@index_blu.route('/')
@user_login_data
def show_index():

    # 上面装饰器的流程：
    # 1.首先在浏览器访问跟路径/，即 http://127.0.0.1:5000
    # 2.进入到@user_login_data，这个装饰起内部，show_index作为参数传给view_func,
    #   执行wrapper方法后，把其中的user添加到g对象中
    # 3.执行代码return view_func(*args,**kwargs)后，返回到show_index方法,
    #   原因是view_func(*args,**kwargs)，即一个函数加括号便是执行这个函数[例如fun()],
    #   也就是执行show_index方法
    # 4.执行方法show_index，便可以使用上面的g.user了,
    #   执行完return render_template("news/index.html",data=data)后，g对象便自动销毁了

    # 用了@user_login_data，这个装饰器之后，下面的代码便可以注释了
    # 1.取出session,中的用户编号
    # user_id = session.get("user_id")

    # 2.获取用户对象
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

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
        "user_info":g.user.to_dict() if g.user else "",
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
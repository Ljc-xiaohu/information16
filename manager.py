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
from info import create_app, db, models  # 导入目的,只是为了让当前项目知道有该文件的存在
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from info.models import User

# 调用业务模块获取app
app = create_app("develop")

# 调用业务模块获取app
manager = Manager(app)

# 使用 Migrate,关联app,db
Migrate(app, db)

# 给manager添加操作命令
manager.add_command("db", MigrateCommand)


# 创建管理员方法
# @manager.option 装饰方法,可以通过命令行的方式调用
#   输入下列代码，例如：（其中admin表示用户名，111111表示密码）
#   python manager.py create_superuser -u admin -p 111111
#   运行玩这行代码，会返回  注册成功
# 参数1: 表示传递的名称   参数2: 是参数名称的解释  参数3: 传递到形式参数的变量
@manager.option('-p', '--password', dest='password')
@manager.option('-u', '--username', dest='username')
def create_superuser(username, password):
    # 1.创建管理员对象
    admin = User()

    # 2.设置属性
    admin.nick_name = username
    admin.password = password
    admin.mobile = username
    admin.is_admin = True

    # 3.保存管理员到数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        return "注册失败"

    return "注册成功"


if __name__ == '__main__':
    manager.run()

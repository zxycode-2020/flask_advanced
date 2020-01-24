# 导入蓝本类库
from flask import Blueprint

# 创建蓝本对象
user = Blueprint('user', __name__)


# 定制路由
@user.route('/login/')
def login():
    return '欢迎登录'

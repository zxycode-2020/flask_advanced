# 导入相关扩展类库
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager


# 创建相关扩展对象
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
login_manager = LoginManager()


# 配置函数
def config_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    # 会话保护级别：
    #  None不使用
    # 'basic'基本级别，默认级别
    # 'strong'用户信息更改立即退出
    login_manager.session_protection = 'strong'
    # 设置登录页面端点，当用户访问需要登录才能访问的页面，
    # 此时还没有登录，会自动跳转到此处
    login_manager.login_view = 'user.login'
    # 设置提示信息，默认是英文提示信息
    login_manager.login_message = '需要登录才可访问'

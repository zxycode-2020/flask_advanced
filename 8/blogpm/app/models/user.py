from flask import current_app
from app.extensions import db, login_manager
# 生成token使用
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 密码散列及校验
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # 指定表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(64), default='default.jpg')
    # 添加关联模型，相当于在关联的模型中动态的添加了一个字段
    # 参数说明：
    # 第一个参数：唯一一个必须的参数，关联的模型类名
    # backref：反向引用的字段名
    # lazy：指定加载关联数据的方式，dynamic:不加载记录，但是提供关联查询
    posts = db.relationship('Posts', backref='user', lazy='dynamic')

    # 保护字段
    @property
    def password(self):
        raise AttributeError('密码是不可读属性')

    # 设置密码，加密存储
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码校验
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成用户激活的token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    # 激活账户时的token校验，校验时还不知道用户信息，需要静态方法
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            # 不存在此用户
            return False
        if not user.confirmed:
            # 账户没有激活时才激活
            user.confirmed = True
            db.session.add(user)
        return True


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

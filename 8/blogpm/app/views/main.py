from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        # 判断是否登录
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            # 根据表单提交的数据常见对象
            p = Posts(content=form.content.data, user=u)
            # 然后写入数据库
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才能发表博客')
            return redirect(url_for('user.login'))
    # 从数据库中读取博客，并分配到模板中，然后在模板中渲染
    # 安装发表时间，降序排列
    # 只获取发表的帖子，过滤回复的帖子
    #posts = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
    # 分页处理
    # 获取当前页码，没有认为是第一页
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=1, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)


@main.route('/jiami/')
def jiami():
    return generate_password_hash('123456')


@main.route('/check/<password>')
def check(password):
    # 密码校验函数：加密后的值  密码
    # 正确：True，错误：False
    if check_password_hash('pbkdf2:sha256:50000$8tHnM54f$c1518c6e491e0a7c5ebd90beb8b56c1d3b03cef66ad940c566578e6a5cfd62ea', password):
        return '密码正确'
    else:
        return '密码错误'


@main.route('/generate_token/')
def generate_token():
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    # 加密指定的数据，已字典的形式传入
    return s.dumps({'id': 250})


@main.route('/activate/<token>')
def activate(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return 'token有误'
    return str(data.get('id'))

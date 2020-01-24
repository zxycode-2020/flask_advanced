from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from app.forms import RegisterForm, LoginForm, PasswordForm
from app.email import send_mail
from app.models import User
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user


user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建对象
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        # 写入数据库
        db.session.add(u)
        # 因为下面产生token时需要用到用户id，此时还没有用户id
        db.session.commit()
        # 生成token
        token = u.generate_activate_token()
        # 发送激活邮件
        send_mail(form.email.data, '账户激活', 'email/account_activate', token=token, username=form.username.data)
        flash('激活邮件已发送，请点击链接完成用户激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('账户激活失败')
        return redirect(url_for('main.index'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('无效的用户名')
        elif u.verify_password(form.password.data):
            # 验证通过，用户登录，顺便可以完成'记住我'的功能
            login_user(u, remember=form.remember_me.data)
            # 如果有下一跳转地址就跳转到指定地址，没有跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
# 保护路由
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')


@user.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_pwd.data):
            current_user.password = form.new_pwd.data
            db.session.add(current_user)
            flash('密码修改成功，下次请使用新密码登录')
            return redirect(url_for('main.index'))
        else:
            flash('无效的原始密码')
            return redirect(url_for('user.change_password'))
    return render_template('user/change_password.html', form=form)

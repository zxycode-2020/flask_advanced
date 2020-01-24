import os
from flask import Flask, render_template, current_app
from flask_script import Manager
# 导入邮件发送相关类库
from flask_mail import Mail, Message
# 导入线程类库
from threading import Thread


app = Flask(__name__)
manager = Manager(app)

# 邮件发送配置，所有的邮件相关配置都必须放在创建对象之前，否则设置不生效
# 邮件服务器
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.1000phone.com'
# 邮件用户名
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'lijie@1000phone.com'
# 邮件密码
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or '1234567890'

# 创建对象
mail = Mail(app)


def async_send_mail(app, msg):
    # 发送邮件需要程序的上下文，否则发送不了邮件
    # 在新的线程中没有上下文，需要手动创建
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    # 从current_app代理对象中获取程序的原始实例
    app = current_app._get_current_object()
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    msg.body = render_template(template + '.txt', **kwargs)
    # 创建线程
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr


@app.route('/')
def index():
    # 调用封装好的邮件发送函数
    send_mail('1256003884@qq.com', '账户激活', 'account', name='pengliang')
    return '邮件发送成功'


if __name__ == '__main__':
    manager.run()

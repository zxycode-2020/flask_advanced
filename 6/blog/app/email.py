from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail
from threading import Thread


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

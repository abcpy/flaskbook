from app import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread


"""
 异步发送email
"""
def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)

def semd_mail(to, subject, template, **kwards):
    # msg = Message('测试邮件', sender='15000728721@163.com', body='Test', recipients=['15000728721@163.com'])
    try:
        msg = Message('[鱼书]' + ' ' + subject, sender=current_app.config['MAIL_SENDER'], 
                            recipients=[to])
        msg.html = render_template(template, **kwards)
        app = current_app._get_current_object()  # 获取flask 核心对象app
        thr = Thread(target=send_async_mail, args=[app, msg])
        thr.start()
    except Exception as e:
        print(e)

    # mail.send(msg)

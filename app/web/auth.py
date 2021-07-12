from flask_login import login_user, logout_user
from wtforms import form
from . import web
from flask import render_template, request, redirect, url_for, flash
from app.forms.register import ResgisterFrom, LoginForm, EmailForm, PasswordForm
from app.models.user import User
from app.models.base import db
from app.libs.email import semd_mail

@web.route('/register', methods=['GET', 'POST'])
def register():
    form = ResgisterFrom(request.form)  # 获取post请求的参数
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            # 数据注册到数据库
            user = User()
            user.set_attr(form.data)
            # 保存模型
            db.session.add(user)
            # db.session.commit()
        return redirect(url_for('web.login'))
        # user.nickname = form.nickname.data
    return render_template('auth/register.html', form=form)

@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # 从数据库中查询用户并校验密码
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 将用户信息写入 cookie 
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
        # 从数据空查询user
    return render_template('auth/login.html', form=form)

@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            user = User.query.filter_by(email=email).first_or_404()
            semd_mail(email,'重置你的密码','email/reset_password.html', user=user, token=user.generate_token())
            flash("邮件已发送，注意查收")
    return render_template('auth/forget_password_request.html', form=form)

@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    print('token', token)
    form = PasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        newpassword = form.password1.data
        success = User.reset_password(token,newpassword)
        if success:
            flash("你的密码已更新，请使用新的密码登录")
            return redirect(url_for('web.login'))
        else:
            flash("密码重置失败")
    return render_template("auth/forget_password.html", form=form)


@web.route('/change/password/', methods=['GET', 'POST'])
def change_password():
    pass

@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))

@web.route('/register/confirm/<token>')
def confirm():
    pass

@web.route('/register/ajax', methods=['GET', 'POST'])
def register_ajax():
    pass



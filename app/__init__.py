from flask.app import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def creare_app():
    app = Flask(__name__)
    print("__name__", __name__)
    # __name__ app
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    mail.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    with app.app_context():
        db.create_all()
    # db.create_all(app=app)
    return app

def register_blueprint(app):
    """
        将blute_print 注册到app对象
    """
    from app.web.book import web
    app.register_blueprint(web)
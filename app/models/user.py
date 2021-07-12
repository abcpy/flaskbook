from app.models.drift import Drift
from itsdangerous.exc import BadSignature, SignatureExpired
from sqlalchemy import Column, Integer, String, Boolean, Float
from app.models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.libs import util
from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db
from app.libs.enums import PendingStatus
from math import floor

class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column("password", String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    sned_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(12))

    """
        属性的get
    """
    @property
    def password(self):
        return self._password
    
    """
         属性的set
    """
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
    
    """
        校验密码
    """
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    """
        校验isbn
        1. 是否符合isbn号规则
        2. 是否存在这个isbn号对应的书
        3. 既不在赠书清单也不在心愿清单才能添加
    """
    def can_save_to_list(self, isbn):
        if util.is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id,isbn=isbn,launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id,isbn=isbn,launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id':self.id}).decode('utf-8')
    
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except SignatureExpired:
            # token 过期
            return False
        except BadSignature:
            # token 错误
            return False
        id = data.get('id')
        user = User.query.get(id)
        if user:
            with db.auto_commit():
                user.password=new_password
                db.session.add(user)
            return True
        else:
            return False

    def can_satisfied_with(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, 
                                           launched=True).count()

        success_receive_count = Drift.query.filter_by(pending=PendingStatus.Success,
                                            requestr_id=self.id).count()
        return True if floor(success_receive_count /2) <= floor(success_gifts_count) else False

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.sned_counter) + '/' + str(self.receive_counter)
        )




@login_manager.user_loader
def login_user(uid):
    return User.query.get(int(uid))




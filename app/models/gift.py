from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Float
from app.models.base import Base
from flask import current_app
from app.spider.yushu_book import YuShuBook
from app import db

class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    
    @classmethod
    def my_gifts(cls, uid):
        my_gifts = Gift.query.filter_by(launched=False, uid=uid).order_by(desc(Gift.create_time)).all()
        return my_gifts
    
    """
    根据传入的一组isbn， 到wish表中检索出相应的礼物，并计算出某个礼物的WIsh心愿数量
    不要在函数中返回元组，返回字典
    """
    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        wishes_count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.isbn.in_(isbn_list), 
            Wish.launched==False,
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{"count":wish_count[0], "isbn":wish_count[1]} for wish_count in wishes_count_list]
        return count_list
  
    """
         查询gift: 
         1. 只显示一定数量（30）
         2. 按照时间的倒序排列，最新的排在最前面
         3. 去重

         对象代表一个礼物，具体的
         类代表礼物这个事情，它是抽象的，不是具体的一个
    """
    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(
              launched=False).group_by(
                  Gift.isbn).order_by(desc(
                  Gift.create_time)).limit(
                  current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
    
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
    
    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False




    
from sqlalchemy import Column, Integer, String, desc, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Float
from app.models.base import Base
from app import db
from app.spider.yushu_book import YuShuBook

class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)
    
    """
    查找我的wishes
    """
    @classmethod
    def myWishes(cls, uid):
        mywishes = Wish.query.filter_by(
            uid=uid,launched=False).order_by(desc(Wish.create_time)).all()
        return mywishes
    
    """
         到GIft表中查到每一本书有多少
         解决循环导入问题
    """
    @classmethod
    def get_wishes_count(cls, isbn_list):
        from app.models.gift import Gift
        wishes_count = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.status == 1,
            Gift.isbn.in_(isbn_list)).group_by(Gift.isbn).all()
        wishesCount = [{"count":wish[0],"isbn":wish[1]} for wish in wishes_count]
        return wishesCount

    @property
    def book(self):
        yushubook = YuShuBook()
        yushubook.search_by_isbn(self.isbn)
        book = yushubook.first
        return book
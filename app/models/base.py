from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, SmallInteger
from contextlib import contextmanager

from sqlalchemy.sql.sqltypes import Integer
from datetime import datetime
from flask_sqlalchemy import BaseQuery


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
            return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)

"""
基类，不需要创建表
"""
class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self) -> None:
        self.create_time = int(datetime.now().timestamp())

    """
        给表中的字段动态赋值
    """
    def set_attr(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
    
    @property
    def create_datatime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
    
    """
       软删除
    """
    def delete(self):
        self.status = 0

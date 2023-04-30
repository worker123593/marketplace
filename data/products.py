import datetime
from sqlalchemy import orm, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Products(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    date_change = Column(DateTime, default=datetime.datetime.now())
    price = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    images_count = Column(Integer, default=1)
    user = orm.relationship('User')

    def __repr__(self):
        return f'{self.id, self.title, self.content, self.price, self.user_id, self.images_count, self.user}'

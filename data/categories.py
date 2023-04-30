from sqlalchemy import Table, Integer, Column, ForeignKey, String
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase

association_table = Table('association', SqlAlchemyBase.metadata,
                          Column('products', Integer, ForeignKey('products.id')),
                          Column('category', Integer, ForeignKey('category.id')))


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

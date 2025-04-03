from sqlalchemy import Column, Integer, ForeignKey
from database.engine import Engine


class ProductCategories(Engine.BASE):
    __tablename__ = 'Product_Categories'

    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), primary_key=True)
    Category_ID = Column(Integer, ForeignKey('Categories.Category_ID'), primary_key=True)

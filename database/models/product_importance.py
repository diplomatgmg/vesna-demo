from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductImportance(Engine.BASE):
    __tablename__ = 'product_importances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.Product_ID'), unique=True)
    importance = Column(Integer, nullable=False)

    product = relationship('Products', back_populates='importance_num')

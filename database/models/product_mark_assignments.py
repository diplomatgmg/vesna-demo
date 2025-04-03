from sqlalchemy import Column, Integer, ForeignKey
from database.engine import Engine


class ProductMarkAssignments(Engine.BASE):
    __tablename__ = 'Product_Mark_Assignments'

    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), primary_key=True)
    Mark_ID = Column(Integer, ForeignKey('Product_Marks.Mark_ID'), primary_key=True)

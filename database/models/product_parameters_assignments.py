from sqlalchemy import Column, Integer, ForeignKey
from database.engine import Engine


class ProductParameterAssignments(Engine.BASE):
    __tablename__ = 'Product_Parameters_Assignments'

    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), primary_key=True)
    Parameter_ID = Column(Integer, ForeignKey('Product_Parameters.Parameter_ID'), primary_key=True)

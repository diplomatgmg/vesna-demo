from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductMarks(Engine.BASE):
    __tablename__ = 'Product_Marks'

    Mark_ID = Column(Integer, primary_key=True)
    Mark_Name = Column(String(16), nullable=False)

    products = relationship('Products', secondary='Product_Mark_Assignments', back_populates='marks')

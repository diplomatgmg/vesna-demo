from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductColors(Engine.BASE):
    __tablename__ = "Colors"
    Color_ID = Column(Integer, primary_key=True, autoincrement=True)
    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), nullable=False)
    Color_Name = Column(String(50), nullable=False)
    Color_Code = Column(String(10), nullable=False)
    Color_image = Column(String(255))
    product = relationship("Products", back_populates="colors")

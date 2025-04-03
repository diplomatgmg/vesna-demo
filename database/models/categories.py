from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.engine import Engine


class Categories(Engine.BASE):
    __tablename__ = 'Categories'

    Category_ID = Column(Integer, primary_key=True, autoincrement=True)
    Category_Name = Column(String(255), nullable=False, unique=False)
    Category_Image = Column(String(255))

    products = relationship("Products", secondary="Product_Categories", back_populates="categories")

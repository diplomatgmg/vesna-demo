from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductImages(Engine.BASE):
    __tablename__ = "Product_Images"
    Image_ID = Column(Integer, primary_key=True, index=True)
    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), nullable=False)
    Image_URL = Column(String, nullable=False)
    MainImage = Column(Boolean, default=False)
    product = relationship("Products", back_populates="images")

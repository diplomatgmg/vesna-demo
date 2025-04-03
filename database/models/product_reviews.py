from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductReviews(Engine.BASE):
    __tablename__ = "Photo_Reviews"

    Photo_ID = Column(Integer, primary_key=True, index=True)
    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), nullable=False)
    Photo_URL = Column(String(255), nullable=False)

    product = relationship("Products", back_populates="reviews")

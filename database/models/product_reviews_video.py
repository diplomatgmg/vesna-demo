from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductReviewsVideo(Engine.BASE):
    __tablename__ = "Video_Reviews"

    Video_ID = Column(Integer, primary_key=True, index=True)
    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), nullable=False)
    Video_URL = Column(String(255), nullable=False)
    Poster_URL = Column(String(256), nullable=True)

    product = relationship("Products", back_populates="reviews_video")

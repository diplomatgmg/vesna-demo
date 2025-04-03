from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database.engine import Engine


class Products(Engine.BASE):
    __tablename__ = "Products"
    Product_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Product_Name = Column(String(255), unique=False, index=True, nullable=False)
    # Price = Column(Integer, nullable=False)
    OnMain = Column(Boolean, default=False)
    # OldPrice = Column(Integer, nullable=True)
    Created_At = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    Updated_At = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    colors = relationship("ProductColors", back_populates="product")
    images = relationship("ProductImages", back_populates="product")
    marks = relationship("ProductMarks",
                         secondary="Product_Mark_Assignments",
                         back_populates="products")
    importance_num = relationship('ProductImportance', back_populates='product', uselist=False)
    categories = relationship("Categories",
                              secondary="Product_Categories",
                              back_populates="products")
    extras = relationship("ProductExtra", back_populates="product")
    reviews = relationship("ProductReviews", back_populates="product")
    reviews_video = relationship("ProductReviewsVideo", back_populates="product")
    parameters = relationship("ProductParameters",
                              secondary="Product_Parameters_Assignments",
                              back_populates="products")

    @property
    def main_image(self):
        return next((image for image in self.images if image.MainImage), None)

    def get_mark_text(self, mark_name):
        mark_texts = {'new': 'New', 'sale': 'Sale', 'hot': 'Hot', 'hit': 'Хит'}
        return mark_texts.get(mark_name, 'Unknown')

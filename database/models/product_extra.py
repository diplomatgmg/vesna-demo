from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductExtra(Engine.BASE):
    __tablename__ = "Product_Extra"

    Product_Extra_ID = Column(Integer, primary_key=True, autoincrement=True)
    Product_ID = Column(Integer, ForeignKey('Products.Product_ID'), nullable=False)
    Characteristics = Column(Text)
    Kit = Column(Text)
    Offer = Column(Text)
    Delivery = Column(Text)

    product = relationship("Products", back_populates="extras")

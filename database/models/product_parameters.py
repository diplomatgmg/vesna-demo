from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.engine import Engine


class ProductParameters(Engine.BASE):
    __tablename__ = 'Product_Parameters'

    Parameter_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)

    parameter_string = Column(String(128), nullable=False, unique=False)
    name = Column(String(64), nullable=False, unique=False)
    price = Column(Integer, nullable=False, unique=False)
    old_price = Column(Integer, nullable=True, unique=False)

    disabled = Column(Boolean, nullable=True, unique=False)
    chosen = Column(Boolean, nullable=True, unique=False)
    extra_field_color = Column(String(128), nullable=True, unique=False)
    extra_field_image = Column(String(512), nullable=True, unique=False)

    products = relationship('Products', secondary='Product_Parameters_Assignments', back_populates='parameters')

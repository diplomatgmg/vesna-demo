from sqlalchemy import Column, Integer, String, Text
from database.engine import Engine


class SpecialProjectParameters(Engine.BASE):
    __tablename__ = "special_project_parameters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, index=True, nullable=False)
    value = Column(String(1024), nullable=False)
    description = Column(Text, nullable=True)
    extra_field_1 = Column(Text, nullable=True)

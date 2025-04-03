from sqlalchemy import Column, Integer, String
from database.engine import Engine


class SpecialProjectParametersBadges(Engine.BASE):
    __tablename__ = "special_project_parameters_badges"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(256), unique=False, index=True, nullable=False)
    image_url = Column(String(256), unique=False, index=True, nullable=False)
    description = Column(String(256), nullable=True)

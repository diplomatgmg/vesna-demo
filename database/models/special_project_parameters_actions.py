from sqlalchemy import Column, Integer, String
from database.engine import Engine


class SpecialProjectParametersActions(Engine.BASE):
    __tablename__ = "special_project_parameters_actions"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(64), nullable=False)
    image_url = Column(String(256), index=True, nullable=True)
    description = Column(String(256), nullable=True)
    extra_field_1 = Column(String(256), nullable=True)
    extra_field_2 = Column(String(256), nullable=True)

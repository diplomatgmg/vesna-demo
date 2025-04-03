import datetime
from sqlalchemy.orm import joinedload
from database.engine import Engine
from database.models.special_project_parameters import SpecialProjectParameters
from database.models.special_project_parameters_badges import SpecialProjectParametersBadges
from database.models.special_project_parameters_actions import SpecialProjectParametersActions
from database.models.categories import Categories
from database.models.products import Products
from database.models.users import Users


class DatabaseCache:
    special_project_parameters_cache = {
        "last_update": None,
        "special_project_parameters": None,
    }
    special_project_parameters_jinja_cache = {}

    special_project_parameters_badges_cache = {
        "last_update": None,
        "special_project_parameters_badges": None,
    }
    special_project_parameters_actions_cache = {
        "last_update": None,
        "special_project_parameters_actions": None,
    }

    categories_cache = {
        "last_update": None,
        "categories": None,
    }
    products_on_main_cache = {
        "last_update": None,
        "products": None,
    }
    products_cache = {
        "last_update": None,
        "products": None,
    }

    @classmethod
    def need_update(cls, data, time: int):
        if data["last_update"] is None or data["last_update"] + time < datetime.datetime.now(
        ).timestamp():
            data["last_update"] = datetime.datetime.now().timestamp()
            return True
        return False

    @classmethod
    def get_special_project_parameters(cls, jinja=False):
        if cls.need_update(cls.special_project_parameters_cache, 300):
            db = Engine.get_db_session()
            spp = db.query(SpecialProjectParameters).all()
            cls.special_project_parameters_cache["special_project_parameters"] = spp
            if spp is not None:
                for parameter in spp:
                    cls.special_project_parameters_jinja_cache[
                        f"{parameter.name}_value"] = parameter.value
                    cls.special_project_parameters_jinja_cache[
                        f"{parameter.name}_description"] = parameter.description
                    cls.special_project_parameters_jinja_cache[
                        f"{parameter.name}_extra_field_1"] = parameter.extra_field_1
            db.remove()
        if jinja:
            return cls.special_project_parameters_jinja_cache
        return cls.special_project_parameters_cache["special_project_parameters"]

    @classmethod
    def get_special_project_parameters_badges(cls):
        if cls.need_update(cls.special_project_parameters_badges_cache, 600):
            db = Engine.get_db_session()
            cls.special_project_parameters_badges_cache[
                "special_project_parameters_badges"] = db.query(
                    SpecialProjectParametersBadges).all()
            db.remove()
        return cls.special_project_parameters_badges_cache["special_project_parameters_badges"]

    @classmethod
    def get_special_project_parameters_actions(cls):
        if cls.need_update(cls.special_project_parameters_actions_cache, 600):
            db = Engine.get_db_session()
            cls.special_project_parameters_actions_cache[
                "special_project_parameters_actions"] = db.query(
                    SpecialProjectParametersActions).all()
            db.remove()
        return cls.special_project_parameters_actions_cache["special_project_parameters_actions"]

    @classmethod
    def get_categories(cls):
        if cls.need_update(cls.categories_cache, 300):
            db = Engine.get_db_session()
            cls.categories_cache["categories"] = db.query(Categories).all()
            db.remove()
        return cls.categories_cache["categories"]

    @classmethod
    def get_products_on_main(cls):
        if cls.need_update(cls.products_on_main_cache, 300):
            db = Engine.get_db_session()
            products = db.query(Products).filter(Products.OnMain == True).options(
                joinedload(Products.images), joinedload(Products.marks),
                joinedload(Products.importance_num), joinedload(Products.categories),
                joinedload(Products.parameters)).all()
            db.remove()
            filtered_products = []
            for product in products:
                product.parameters = [p for p in product.parameters if not p.disabled and p.chosen]
                if len(product.parameters) > 0:
                    filtered_products.append(product)
            cls.products_on_main_cache["products"] = filtered_products
        return cls.products_on_main_cache["products"]

    @classmethod
    def get_products(cls):
        if cls.need_update(cls.products_cache, 300):
            db = Engine.get_db_session()
            products = db.query(Products).options(joinedload(Products.images),
                                                  joinedload(Products.marks),
                                                  joinedload(Products.importance_num),
                                                  joinedload(Products.categories),
                                                  joinedload(Products.parameters)).all()
            db.remove()
            filtered_products = []
            for product in products:
                product.parameters = [p for p in product.parameters if not p.disabled and p.chosen]
                if len(product.parameters) > 0:
                    filtered_products.append(product)
            cls.products_cache["products"] = filtered_products
        return cls.products_cache["products"]

    @classmethod
    def get_product_by_id(cls, product_id):
        db = Engine.get_db_session()
        product = db.query(Products).filter(Products.Product_ID == product_id).options(
            joinedload(Products.images), joinedload(Products.colors), joinedload(Products.extras),
            joinedload(Products.reviews), joinedload(Products.reviews_video),
            joinedload(Products.parameters)).one_or_none()
        db.remove()
        if product:
            product.parameters = [p for p in product.parameters if not p.disabled]
        return product

    @classmethod
    def add_user(cls,
                 t_user_id,
                 t_username=None,
                 t_first_name=None,
                 t_last_name=None,
                 t_is_premium=False,
                 password=None,
                 email=None,
                 phone=None) -> bool:
        db = Engine.get_db_session()
        user = db.query(Users).filter(Users.t_user_id == t_user_id).one_or_none()
        if user is None:
            user = Users(t_user_id=t_user_id,
                         t_username=t_username,
                         t_first_name=t_first_name,
                         t_last_name=t_last_name,
                         t_is_premium=t_is_premium,
                         password=password,
                         email=email,
                         phone=phone)
            db.add(user)
            db.commit()
            db.remove()
            return True
        db.remove()
        return False

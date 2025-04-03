from flask import Blueprint, render_template
from database.cache import DatabaseCache
from comon_functions.lprint import lprint
from config.config import PROJECT_RANDOM_ID


index_router = Blueprint("index_router", __name__)


@index_router.route("/", methods=["GET"])
def main_page():
    try:
        products = DatabaseCache.get_products_on_main()
        categories = DatabaseCache.get_categories()
        actions = DatabaseCache.get_special_project_parameters_actions()
        
        products.sort(key=lambda product: product.importance_num.importance
                      if product.importance_num else 0,
                      reverse=True)
        context = {
            "title": "Главная страница",
            "meta_description": "Главная страница",
            "meta_keywords": "main, page",
            "project_random_id": PROJECT_RANDOM_ID,
            "SPP_badges": DatabaseCache.get_special_project_parameters_badges(),
            "products": products,
            "categories": categories,
            "page": "main",
            "actions": actions
        }
        context.update(DatabaseCache.get_special_project_parameters(jinja=True))

    except Exception as e:
        lprint.p("Error on index page", e)
        return render_template("error.html")

    return render_template("index.html", **context)

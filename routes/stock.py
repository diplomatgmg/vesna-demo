from flask import Blueprint, render_template
from database.cache import DatabaseCache
from comon_functions.lprint import lprint
from config.config import PROJECT_RANDOM_ID


stock_router = Blueprint("stock_router", __name__)


@stock_router.route("/stock", methods=["GET"])
def stock_page():
    try:
        context = {
            "title": "Акции",
            "meta_description": "Наши акции",
            "meta_keywords": "actions, page",
            "project_random_id": PROJECT_RANDOM_ID,
            "page": "stock",
            "SPP_actions": DatabaseCache.get_special_project_parameters_actions(),
        }
        context.update(DatabaseCache.get_special_project_parameters(jinja=True))

    except Exception as e:
        lprint.p("Error on product page", e)
        return render_template("error.html")

    return render_template("stock.html", **context)

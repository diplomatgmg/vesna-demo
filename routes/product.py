from flask import Blueprint, render_template, redirect
from database.cache import DatabaseCache
from comon_functions.lprint import lprint
from config.config import PROJECT_RANDOM_ID

product_router = Blueprint("product_router", __name__)


@product_router.route("/product/<int:product_id>", methods=["GET"])
def product_page(product_id):
    try:
        product = DatabaseCache.get_product_by_id(product_id)
        chosen_parameter = None
        product.parameters = sorted(product.parameters, key=lambda x: x.Parameter_ID)
        for indx, parameter in enumerate(product.parameters):
            print(indx, parameter.Parameter_ID)
            if parameter.chosen:
                chosen_parameter = indx
                break
        if not product or chosen_parameter is None:
            lprint.p("Error on product page, product not found")
            return redirect("/")
        context = {
            "title": "Продукт",
            "meta_description": "Сведения о товаре",
            "meta_keywords": "product, page",
            "project_random_id": PROJECT_RANDOM_ID,
            "page": "product",
            "SPP_badges": DatabaseCache.get_special_project_parameters_badges(),
            "product": product,
            "chosen_parameter": chosen_parameter,
        }
        context.update(DatabaseCache.get_special_project_parameters(jinja=True))


    except Exception as e:
        lprint.p("Error on product page", e)
        return render_template("error.html")

    return render_template("product.html", **context)

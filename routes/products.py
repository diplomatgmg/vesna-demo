from flask import Blueprint, render_template, request
from pydantic import ValidationError
from database.cache import DatabaseCache
from pydantic_store.schemas import ProductQueryParams
from comon_functions.lprint import lprint
from config.config import PROJECT_RANDOM_ID


products_router = Blueprint("products_router", __name__)


@products_router.route("/products", methods=["GET"])
def products_page():
    try:
        query_params = ProductQueryParams(**request.args)
        products = DatabaseCache.get_products()
        markorchip_present = bool(query_params.mark or query_params.chip)
        search_present = bool(query_params.search)

        if query_params.chip:
            p_copy = products.copy()
            p_copy.sort(key=lambda p: p.parameters[0].price)
            products = p_copy

        if query_params.mark or query_params.category or query_params.search:
            new_products = []
            for product in products:
                if query_params.mark and query_params.mark in [mark.Mark_Name for mark in product.marks]:
                    new_products.append(product)
                elif query_params.category and query_params.category in [category.Category_ID for category in product.categories]:
                    new_products.append(product)
                elif query_params.search and query_params.search.lower() in product.Product_Name.lower():
                    new_products.append(product)
            products = new_products

        context = {
            "title": "Продукты",
            "meta_description": "Каталог товаров",
            "meta_keywords": "products, page",
            "project_random_id": PROJECT_RANDOM_ID,
            "page": "products",
            "SPP_badges": DatabaseCache.get_special_project_parameters_badges(),
            "categories": DatabaseCache.get_categories(),
            "products": products,
            "markorchip_present": markorchip_present,
            "search_present": search_present,
        }
        context.update(DatabaseCache.get_special_project_parameters(jinja=True))

    except ValidationError as e:
        lprint.p("Validation Error:", e)
        return render_template("error.html", error_message=e), 400

    except Exception as e:
        lprint.p("Error on product page", e)
        return render_template("error.html")

    return render_template("products.html", **context)

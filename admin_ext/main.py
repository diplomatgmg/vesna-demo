from flask_basicauth import BasicAuth
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from app import fl_app

from database.engine import Engine
from database.models.special_project_parameters import SpecialProjectParameters
from database.models.special_project_parameters_badges import SpecialProjectParametersBadges
from database.models.special_project_parameters_actions import SpecialProjectParametersActions
from database.models.products import Products
from database.models.product_images import ProductImages
from database.models.product_colors import ProductColors
from database.models.product_marks import ProductMarks
from database.models.product_parameters import ProductParameters
from database.models.product_mark_assignments import ProductMarkAssignments
from database.models.product_parameters_assignments import ProductParameterAssignments
from database.models.product_importance import ProductImportance
from database.models.categories import Categories
from database.models.product_categories import ProductCategories
from database.models.product_extra import ProductExtra
from database.models.product_reviews import ProductReviews
from database.models.product_reviews_video import ProductReviewsVideo
from database.models.users import Users


basic_auth = BasicAuth(fl_app)


class AuthenticatedModelView(ModelView):

    def is_accessible(self):
        return basic_auth.authenticate()


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @basic_auth.required
    def index(self):
        return super().index()


class FlaskAdmin:
    fl_admin = Admin(fl_app, name='APP', template_mode='bootstrap4', index_view=MyAdminIndexView())

    @classmethod
    def init(cls):
        from admin_ext.overrides import ProductImagesView
        from admin_ext.overrides import ProductsView
        from admin_ext.overrides import ProductExtraView
        from admin_ext.overrides import ProductColorsView
        from admin_ext.overrides import ProductReviewsView
        from admin_ext.overrides import ProductReviewsVideoView
        from admin_ext.overrides import ProductImportanceView
        from admin_ext.overrides import ProductCategoriesView
        from admin_ext.overrides import ProductMarksView
        from admin_ext.overrides import ProductParametersView
        from admin_ext.overrides import ProductMarkAssignmentsView
        from admin_ext.overrides import ProductCategoriesAssignmentsView
        from admin_ext.overrides import ProductParametersAssignmentsView
        from admin_ext.overrides import SpecialProjectParametersView
        from admin_ext.overrides import SpecialProjectParametersBadgesView
        from admin_ext.overrides import SpecialProjectParametersActionsView
        from admin_ext.overrides import UsersView

        cls.fl_admin.add_view(ProductsView(Products, Engine.get_db_session()))

        cls.fl_admin.add_view(ProductImagesView(ProductImages, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductColorsView(ProductColors, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductExtraView(ProductExtra, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductReviewsView(ProductReviews, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductReviewsVideoView(ProductReviewsVideo, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductImportanceView(ProductImportance, Engine.get_db_session()))

        cls.fl_admin.add_view(ProductCategoriesView(Categories, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductMarksView(ProductMarks, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductParametersView(ProductParameters, Engine.get_db_session()))

        cls.fl_admin.add_view(ProductMarkAssignmentsView(ProductMarkAssignments, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductCategoriesAssignmentsView(ProductCategories, Engine.get_db_session()))
        cls.fl_admin.add_view(ProductParametersAssignmentsView(ProductParameterAssignments, Engine.get_db_session()))

        cls.fl_admin.add_view(SpecialProjectParametersView(SpecialProjectParameters, Engine.get_db_session()))
        cls.fl_admin.add_view(SpecialProjectParametersBadgesView(SpecialProjectParametersBadges, Engine.get_db_session()))
        cls.fl_admin.add_view(SpecialProjectParametersActionsView(SpecialProjectParametersActions, Engine.get_db_session()))

        cls.fl_admin.add_view(UsersView(Users, Engine.get_db_session()))

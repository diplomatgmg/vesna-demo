from flask_admin.contrib.sqla import ModelView
from admin_ext.main import basic_auth
from database.engine import Engine


def renew_session(session):
    # print("removing session", session) # забыли убрать
    session.close()
    return Engine.get_fla_session()


class BaseModelView(ModelView):
    def is_accessible(self):
        self.session = renew_session(self.session)
        return basic_auth.authenticate()

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()


class ProductsView(BaseModelView):
    form_columns = ['Product_Name', 'OnMain', 'Created_At', 'Updated_At']
    column_list = [
        'Product_ID', 'Product_Name', 'OnMain', 'Created_At', 'Updated_At'
    ]
    can_create = True
    column_default_sort = 'Product_ID'


class ProductImagesView(BaseModelView):
    form_columns = ['Product_ID', 'Image_URL', 'MainImage']
    column_list = ['Product_ID', 'Image_URL', 'MainImage']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductExtraView(BaseModelView):
    form_columns = ['Product_ID', 'Characteristics', 'Kit', 'Offer', 'Delivery']
    column_list = ['Product_ID', 'Characteristics', 'Kit', 'Offer', 'Delivery']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductColorsView(BaseModelView):
    form_columns = ['Product_ID', 'Color_Name', 'Color_Code', 'Color_image']
    column_list = ['Product_ID', 'Color_Name', 'Color_Code', 'Color_image']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductReviewsView(BaseModelView):
    form_columns = ['Product_ID', 'Photo_URL']
    column_list = ['Product_ID', 'Photo_URL']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductReviewsVideoView(BaseModelView):
    form_columns = ['Product_ID', 'Video_URL', 'Poster_URL']
    column_list = ['Product_ID', 'Video_URL', 'Poster_URL']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductImportanceView(BaseModelView):
    form_columns = ['product_id', 'importance']
    column_list = ['product_id', 'importance']
    can_create = True
    column_default_sort = 'product_id'


class ProductCategoriesView(BaseModelView):
    form_columns = ['Category_Name', 'Category_Image']
    column_list = ['Category_ID', 'Category_Name', 'Category_Image']
    can_create = True
    column_default_sort = 'Category_ID'


class ProductMarksView(BaseModelView):
    form_columns = ['Mark_Name']
    column_list = ['Mark_ID', 'Mark_Name']
    can_create = True
    column_default_sort = 'Mark_ID'


class ProductParametersView(BaseModelView):
    form_columns = [
        'parameter_string', 'name', 'price', 'old_price', 'disabled', 'chosen', 'extra_field_color',
        'extra_field_image'
    ]
    column_list = [
        'Parameter_ID', 'parameter_string', 'name', 'price', 'old_price', 'disabled', 'chosen',
        'extra_field_color', 'extra_field_image'
    ]
    can_create = True
    column_default_sort = 'Parameter_ID'


class ProductMarkAssignmentsView(BaseModelView):
    form_columns = ['Product_ID', 'Mark_ID']
    column_list = ['Product_ID', 'Mark_ID']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductCategoriesAssignmentsView(BaseModelView):
    form_columns = ['Product_ID', 'Category_ID']
    column_list = ['Product_ID', 'Category_ID']
    can_create = True
    column_default_sort = 'Product_ID'


class ProductParametersAssignmentsView(BaseModelView):
    form_columns = ['Product_ID', 'Parameter_ID']
    column_list = ['Product_ID', 'Parameter_ID']
    can_create = True
    column_default_sort = 'Product_ID'


class SpecialProjectParametersView(BaseModelView):
    form_columns = ['value', 'description', 'extra_field_1']
    column_list = ['id', 'name', 'value', 'description', 'extra_field_1']
    can_create = False
    can_delete = False
    column_default_sort = 'id'


class SpecialProjectParametersBadgesView(BaseModelView):
    form_columns = ['url', 'image_url', 'description']
    column_list = ['id', 'url', 'image_url', 'description']
    can_create = True
    can_delete = True
    column_default_sort = 'id'


class SpecialProjectParametersActionsView(BaseModelView):
    form_columns = ['action_type', 'image_url', 'description', 'extra_field_1', 'extra_field_2']
    column_list = ['id', 'action_type', 'image_url', 'description', 'extra_field_1', 'extra_field_2']
    can_create = True
    can_delete = True
    column_default_sort = 'id'


class UsersView(BaseModelView):
    form_columns = ['t_username', 't_first_name', 't_last_name', 't_is_premium', 'email', 'phone']
    column_list = ['id', 't_user_id', 't_username', 't_first_name', 't_last_name', 't_is_premium', 'email', 'phone', 'Created_At', 'Updated_At']
    can_create = False
    can_delete = False
    can_edit = False
    column_default_sort = 'id'

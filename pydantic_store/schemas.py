import re
from pydantic import BaseModel, field_validator


class ProductQueryParams(BaseModel):
    search: str | None = None
    mark: str | None = None
    chip: bool | None = None
    category: int | None = None

    @field_validator('mark')
    def validate_mark(cls, value):
        if value is not None:
            if not value.isalpha():
                raise ValueError("Mark must contain only letters.")
            if len(value) > 16:
                raise ValueError("Mark cannot exceed 16 characters.")
        return value

    @field_validator('search')
    def validate_search(cls, value):
        if value is not None:
            if not re.fullmatch(r"[\w\d ]+", value, re.UNICODE) and value != "":
                raise ValueError("string must contain only letters.")
            if len(value) > 256:
                raise ValueError("Mark cannot exceed 256 characters.")
        return value


class CartFormItems(BaseModel):
    fio: str
    phone: str
    city: str
    house: str
    apartment: str | None = None
    comment: str | None = None
    # payment_method: str
    payment_type: str
    tg_user_id: int | None = None

    # @field_validator('phone')
    # def validate_phone(cls, value):
    #     if not re.match(r"^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$", value):
    #         raise ValueError("Invalid phone number format. Use +7(000)000-00-00.")
    #     return value

    @field_validator('fio', 'phone', 'city', 'house', 'apartment', 'comment')
    def validate_length(cls, value, field):
        max_length = 1024
        if len(value) > max_length:
            raise ValueError(f"{field.name.capitalize()} cannot exceed {max_length} characters.")
        return value

    @field_validator('tg_user_id')
    def validate_tg_user_id(cls, value):
        if value is not None and int(value) < 1:
            raise ValueError("Errror incorrect tg_user_id")
        return value


class CartFromProductData(BaseModel):
    product_id: int
    parameter_id: int
    quantity: int

    @field_validator('product_id', 'parameter_id', 'quantity')
    def validate_numbers(cls, value):
        if int(value) < 1:
            raise ValueError("Error incorrect id or quantity or something else")
        return value

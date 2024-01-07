from typing import Optional, Type, Any

from apps.core.database import Base
from apps.core.exceptions import OrmValidationError


def extract_query_param(request, param: str, type_to_cast: Optional[Type] = None, default_value: Any = None):
    value = request.query.get(param, default_value)
    if not type_to_cast:
        return value
    try:
        return type_to_cast(value)
    except (TypeError, ValueError):
        return default_value


def get_column_orm(model_object: Type[Base], column: str):
    if not isinstance(model_object, Base):
        raise OrmValidationError(f'{model_object} is not sqlalchemy model')
    column_orm = getattr(model_object, column)
    if not column:
        raise OrmValidationError(f'{column} not exists')
    return column_orm

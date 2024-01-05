from typing import Optional, Type, Any


def extract_query_param(request, param: str, type_to_cast: Optional[Type] = None, default_value: Any = None):
    value = request.query.get(param, default_value)
    if not type_to_cast:
        return value
    try:
        return type_to_cast(value)
    except (TypeError, ValueError):
        return default_value

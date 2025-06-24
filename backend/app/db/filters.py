from sqlalchemy.sql import operators
from sqlalchemy import and_

OPERATOR_MAPPING = {
    "eq": operators.eq,
    "neq": operators.ne,
    "lt": operators.lt,
    "lte": operators.le,
    "gt": operators.gt,
    "gte": operators.ge,
    "like": lambda col, val: col.like(f"%{val}%"),
    "ilike": lambda col, val: col.ilike(f"%{val}%"),
    "in": lambda col, val: col.in_(val.split(",")),
}

def parse_filters(model, query_params):
    filters = []
    for key, value in query_params.items():
        if not key.startswith("filter["):
            continue
        try:
            key_inner = key[7:-1]
            if "][" in key_inner:
                field, op = key_inner.split("][")
                column = getattr(model, field, None)
                if column and op in OPERATOR_MAPPING:
                    filters.append(OPERATOR_MAPPING[op](column, value))
        except:
            continue
    return and_(*filters) if filters else True

def require_fields(data, fields):
    missing = [f for f in fields if not str(data.get(f, "")).strip()]
    return missing

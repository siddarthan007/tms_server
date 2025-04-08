def validate_positive(value: int, field_name: str):
    if value <= 0:
        raise ValueError(f"{field_name} must be positive")
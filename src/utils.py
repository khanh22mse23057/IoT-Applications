def parse_value(value, data_type):
    try:
        parsed_value = data_type(value)
        return parsed_value
    except ValueError:
        return None
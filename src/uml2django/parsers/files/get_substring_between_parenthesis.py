def get_sub_string_between_parenthesis(full_string: str) -> str:
    return full_string[
        full_string.find("(")+1:full_string.find(")")
    ]

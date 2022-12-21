def _is_number(x) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False


def _prefix_to_infix_render(tokens: list[str], index: int) -> tuple[str, int]:
    token = tokens[index]
    match token:
        case number if _is_number(number) or number == "x":
            return number, index + 1
        case operation if operation in ("+", "-", "*", "/", "="):
            left_value, updated_index = _prefix_to_infix_render(tokens, index + 1)
            right_value, updated_index = _prefix_to_infix_render(tokens, updated_index)
            return f"({left_value}) {operation} ({right_value})", updated_index
        case unknown:
            raise ValueError(f"Unknown: {unknown}")


def prefix_to_infix(tokens: list[str]) -> str:
    return _prefix_to_infix_render(tokens, 0)[0]

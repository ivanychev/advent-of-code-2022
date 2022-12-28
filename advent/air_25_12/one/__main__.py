import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

digit_to_value = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}
value_to_digit = {
    v: k for k, v in digit_to_value.items()
}


def decode_number(s: str) -> int:
    power = 0
    total = 0
    for c in reversed(s):
        total += digit_to_value[c] * (5 ** power)
        power += 1
    return total


def encode_number(n: int) -> str:
    digits = []
    while n:
        n, left = divmod(n, 5)
        digits.append(left)

    new_digits = []
    left = 0
    for digit in digits:
        digit = digit + left
        left = 0
        new_digit = digit
        if digit > 2:
            new_digit = value_to_digit[digit - 5]
            left = 1
        new_digits.append(str(new_digit))
    return "".join(reversed(new_digits))


if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        print(encode_number(sum(
            decode_number(s.strip())
            for s in f
        )))

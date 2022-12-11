from typing import TextIO

from advent.no_space_left_12_07.token import Token


def read_tokens(f: TextIO) -> list[Token]:
    token = []
    for line in f:
        token.append(Token.parse_line(line))
    return token

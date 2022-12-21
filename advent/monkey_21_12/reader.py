import operator
import re
from typing import Callable, TextIO

from monkey_21_12.monkey import Monkey
from monkey_21_12.operation import BinaryOperation, Number, Variable

MONKEY_RE = re.compile(r"^(?P<name>\w+): (?P<op>.*)$")


def _is_number(x) -> bool:
    try:
        int(x)
        return True
    except ValueError:
        return False


def _op_from_raw_op(op: str) -> Callable[[float, float], float]:
    match op:
        case "+":
            return operator.add
        case "-":
            return operator.sub
        case "*":
            return operator.mul
        case "/":
            return operator.truediv
        case "==":
            return operator.eq
        case unknown:
            raise ValueError(f"Invalid op: {op}")


def read_monkeys(
    f: TextIO, part_2: bool = False
) -> tuple[list[Monkey], dict[str, Monkey]]:
    monkeys = []
    monkey_registry = {}
    for row in f:
        m = MONKEY_RE.match(row).groupdict()
        name = m["name"]
        op = m["op"]

        if _is_number(op):
            if name == "humn":
                monkey = Monkey(name=name, op=Variable())
            else:
                monkey = Monkey(name=name, op=Number(int(op)))
        else:
            left, raw_op, right = op.split(" ", maxsplit=2)
            if part_2 and name == "root":
                raw_op = "=="
            monkey = Monkey(
                name=name,
                op=BinaryOperation(
                    left_name=left, right_name=right, op=_op_from_raw_op(raw_op)
                ),
            )
        monkeys.append(monkey)
        monkey_registry[monkey.name] = monkey
    return monkeys, monkey_registry

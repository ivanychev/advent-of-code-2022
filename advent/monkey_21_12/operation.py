import dataclasses
import operator
from typing import Callable


@dataclasses.dataclass(frozen=True, slots=True)
class EvalResult:
    value: float
    count: int


class Operation:
    def eval(self, monkey_registry: dict[str, "Monkey"]) -> EvalResult:
        pass

    def render(self, monkey_registry: dict[str, "Monkey"], stack: list[str]):
        pass


@dataclasses.dataclass
class Number(Operation):
    value: float

    def eval(self, monkey_registry: dict[str, "Monkey"]) -> EvalResult:
        return EvalResult(self.value, 1)

    def render(self, monkey_registry: dict[str, "Monkey"], stack: list[str]):
        stack.append(str(self.value))


@dataclasses.dataclass
class Variable(Operation):
    value: float | None = None

    def eval(self, monkey_registry: dict[str, "Monkey"]) -> EvalResult:
        if self.value is None:
            raise ValueError("Variable is not set")
        return EvalResult(self.value, 1)

    def render(self, monkey_registry: dict[str, "Monkey"], stack: list[str]):
        stack.append("x")


@dataclasses.dataclass
class BinaryOperation(Operation):
    left_name: str
    right_name: str
    op: Callable[[float, float], float]

    def eval(self, monkey_registry: dict[str, "Monkey"]) -> EvalResult:
        left_res = monkey_registry[self.left_name].op.eval(monkey_registry)
        right_res = monkey_registry[self.right_name].op.eval(monkey_registry)
        return EvalResult(
            value=self.op(left_res.value, right_res.value),
            count=left_res.count + right_res.count + 1,
        )

    def render(self, monkey_registry: dict[str, "Monkey"], stack: list[str]):
        match self.op:
            case operator.add:
                stack.append("+")
            case operator.sub:
                stack.append("-")
            case operator.mul:
                stack.append("*")
            case operator.truediv:
                stack.append("/")
            case operator.eq:
                stack.append("=")
            case unknown:
                raise ValueError(f"unknown op {self.op}")
        monkey_registry[self.left_name].op.render(monkey_registry, stack)
        monkey_registry[self.right_name].op.render(monkey_registry, stack)

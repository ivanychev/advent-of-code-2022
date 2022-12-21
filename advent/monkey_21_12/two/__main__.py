import pathlib
import textwrap

from monkey_21_12.reader import read_monkeys
from monkey_21_12.render import prefix_to_infix
from sympy import sympify

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        monkeys, monkey_registry = read_monkeys(f, part_2=True)
        rendered = []
        monkey_registry["root"].op.render(monkey_registry, rendered)
        # print(rendered)
        rendered_eq = prefix_to_infix(rendered)
        left, right = rendered_eq.split("=")

        exec(
            textwrap.dedent(
                f"""\
        from sympy.abc import x
        from sympy import solve

        print(solve({left} - {right}, dict=True))
        """
            )
        )

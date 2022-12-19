import concurrent.futures
import operator
import pathlib
from functools import reduce

from minerals_19_12.blueprint import Blueprint
from minerals_19_12.reader import read_blueprints
from minerals_19_12.strategy import StrategyOptimizer
from tqdm import tqdm

CURRENT_DIR = pathlib.Path(__file__).parent

RUNNING_TIME = 32


def find_best_strategy(b: Blueprint):
    opt = StrategyOptimizer(b, RUNNING_TIME)
    return opt.best_strategy()


if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        blueprints = read_blueprints(f)[:3]

        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as ex:
            best_strategies = list(tqdm(ex.map(find_best_strategy, blueprints)))
        print(reduce(operator.mul, (s.geode for s in best_strategies)))

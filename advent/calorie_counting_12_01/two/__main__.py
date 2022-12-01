import pathlib

from advent.calorie_counting_12_01.inventory import read_elves
from heapq import heapify, heappop

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        elves = read_elves(f)
        calories = [-e.sum_calories for e in elves]
        heapify(calories)

        print(-(heappop(calories) + heappop(calories) + heappop(calories)))

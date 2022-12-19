from collections import deque
from operator import attrgetter

from minerals_19_12.blueprint import Blueprint
from minerals_19_12.factory import FactoryState


class StrategyOptimizer:
    def __init__(self, blueprint: Blueprint, time_minutes: int):
        self.blueprint = blueprint
        self.time_minutes = time_minutes

    def best_strategy(self) -> FactoryState:
        best_strategy: FactoryState | None = None
        f = FactoryState(blueprint=self.blueprint, ore_robots=1)
        visited = set()
        max_time = 0

        q = deque([f])
        while q:
            state = q.popleft()
            if state.time != max_time:
                max_time = state.time
            if state in visited:
                continue
            visited.add(state)

            if state.time == self.time_minutes:
                best_strategy = (
                    state
                    if not best_strategy
                    else max(best_strategy, state, key=attrgetter("geode"))
                )
            else:
                states = [s for s in state.next_states() if s not in visited]
                assert all(s.time == state.time + 1 for s in states)
                q.extend(states)
        return best_strategy

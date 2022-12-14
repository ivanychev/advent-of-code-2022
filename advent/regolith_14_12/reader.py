from typing import TextIO

from advent.regolith_14_12.field import RockField


def read_rocks(f: TextIO) -> RockField:
    traces = []
    for raw_trace in f:
        raw_trace = raw_trace.strip()
        traces.append(raw_trace)
    field = RockField()
    field.fill_rock_from_traces(traces)
    return field

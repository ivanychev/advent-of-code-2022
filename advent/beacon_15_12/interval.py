def join_intervals(intervals: list[tuple[int, int]]):
    intervals = intervals[::-1]
    result = []
    while len(intervals) > 1:
        first = intervals.pop()
        second = intervals.pop()

        if second[0] > first[1]:
            result.append(first)
            intervals.append(second)
            continue
        else:
            intervals.append((first[0], max(first[1], second[1])))
    if intervals:
        result.extend(intervals)
    return result

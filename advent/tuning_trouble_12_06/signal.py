from collections import Counter, deque
from typing import NamedTuple

MARKER_SIZE = 4
MESSAGE_SIZE = 14


class Signal(NamedTuple):
    value: str

    def find_first_marker(self) -> int:
        return self.find_unique_chars(MARKER_SIZE)

    def find_first_message(self) -> int:
        return self.find_unique_chars(MESSAGE_SIZE)

    def find_unique_chars(self, unique_length: int) -> int:
        queue = deque(self.value[:unique_length])
        c = Counter(queue)
        consumed = unique_length
        string_iterator = iter(self.value[unique_length:])
        while len(c) != unique_length:
            # Remove char
            removed = queue.popleft()
            c[removed] -= 1
            if not c[removed]:
                del c[removed]

            # Add char
            next_char = next(string_iterator)
            queue.append(next_char)
            c.update(next_char)
            consumed += 1
        return consumed


if __name__ == "__main__":
    print(Signal("bvwbjplbgvbhsrlpgdmjqwftvncz").find_first_marker())
    print(Signal("nppdvjthqldpwncqszvftbrmjlhg").find_first_marker())
    print(Signal("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg").find_first_marker())
    print(Signal("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw").find_first_marker())

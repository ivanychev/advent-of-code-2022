import abc
from typing import Callable

CycleCallback = Callable[["Cpu", int], None]


class Command(abc.ABC):
    @abc.abstractmethod
    def execution_time(self):
        pass

    @abc.abstractmethod
    def action(self, cpu: "Cpu"):
        pass


class Cpu:
    def __init__(self):
        self.clock = 0
        self.X = 1
        self._cur_cmd_clock = 0
        self._cur_cmd: Command | None = None
        self._during_cycle_callback: CycleCallback | None = None

    def _current_command_finished(self):
        return (
            not self._cur_cmd or self._cur_cmd_clock == self._cur_cmd.execution_time()
        )

    def _apply_action(self):
        if self._cur_cmd:
            self._cur_cmd.action(self)

    def with_during_cycle_callback(self, callback: CycleCallback):
        self._during_cycle_callback = callback
        return self

    def _call_during_cycle_callback(self, cycle_index: int):
        if self._during_cycle_callback:
            self._during_cycle_callback(self, cycle_index)

    def execute(self, commands: list[Command]):
        commands = commands[::-1]
        while commands or not self._current_command_finished():
            cycle_index = self.clock + 1

            # Cycle in progress
            if self._current_command_finished():
                self._cur_cmd = commands.pop()
                self._cur_cmd_clock = 0
            self._call_during_cycle_callback(cycle_index)

            # Cycle finished
            self.clock = cycle_index
            self._cur_cmd_clock += 1
            if self._current_command_finished():
                self._apply_action()


class Addx(Command):
    def __init__(self, value: int):
        self.value = value

    def execution_time(self):
        return 2

    def action(self, cpu: "Cpu"):
        cpu.X += self.value


class Noop(Command):
    def execution_time(self):
        return 1

    def action(self, cpu: "Cpu"):
        pass

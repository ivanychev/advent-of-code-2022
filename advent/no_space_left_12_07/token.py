import abc
import dataclasses
from abc import ABC

from typing_extensions import Self


def _is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


class Token(ABC):
    @abc.abstractmethod
    def is_command(self) -> bool:
        pass

    @classmethod
    def parse_line(cls, s: str) -> Self:
        s = s.strip()
        if s.startswith("$ cd"):
            return Cd.parse_line(s)
        if s == "$ ls":
            return Ls()
        if s.startswith("dir "):
            return Dir.parse_line(s)
        if _is_int(s.split(" ", maxsplit=1)[0]):
            return File.parse_line(s)
        raise ValueError(f"Invalid line '{s}'")


@dataclasses.dataclass
class Cd(Token):
    target: str

    def is_command(self) -> bool:
        return True

    @classmethod
    def parse_line(cls, s: str) -> Self:
        _, cmd, name = s.split(" ")
        return cls(target=name)


@dataclasses.dataclass
class Ls(Token):
    def is_command(self) -> bool:
        return True


@dataclasses.dataclass
class File(Token):
    name: str
    size: int

    def is_command(self) -> bool:
        return False

    @classmethod
    def parse_line(cls, s: str) -> Self:
        size, name = s.split(" ", maxsplit=1)
        return cls(name=name, size=int(size))


@dataclasses.dataclass
class Dir(Token):
    name: str

    def is_command(self) -> bool:
        return False

    @classmethod
    def parse_line(cls, s: str) -> Self:
        _, name = s.split(" ", maxsplit=1)
        return cls(name=name)

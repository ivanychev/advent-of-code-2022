import abc
import dataclasses
from abc import ABC
from itertools import islice
from typing import Callable, Iterable

from typing_extensions import Self

from advent.no_space_left_12_07.token import Cd, Dir, File, Ls, Token

CommandPointer = int


class Node(ABC):
    def is_directory(self):
        return isinstance(self, DirectoryNode)

    @abc.abstractmethod
    def size(self) -> int:
        pass

    @abc.abstractmethod
    def visit(
        self, predicate: Callable[[Self], bool], callback: Callable[[Self], None]
    ):
        pass


@dataclasses.dataclass
class FileNode(Node):
    name: str
    file_size: int

    def size(self) -> int:
        return self.file_size

    def visit(
        self, predicate: Callable[[Node], bool], callback: Callable[[Node], None]
    ):
        if not predicate(self):
            return
        callback(self)


def _consume_ls_output(
    tokens: list[Token], ls_command_pointer: CommandPointer
) -> (CommandPointer, Iterable[Token]):
    pointer = ls_command_pointer + 1
    while pointer < len(tokens) and isinstance(tokens[pointer], (File, Dir)):
        pointer += 1
    return pointer, islice(tokens, ls_command_pointer + 1, pointer)


@dataclasses.dataclass
class DirectoryNode(Node):
    def __init__(self, dir_name: str, parent: Self | None):
        self.dir_name = dir_name
        self.scanned = False
        self.parent = parent
        self.children: dict[str, Node] = {}
        self.frozen = False
        self._cached_size = None

    def size(self) -> int:
        if not self.frozen:
            raise ValueError("The tree is being mutated, size can't be computed")
        if self._cached_size is None:
            self._cached_size = sum(c.size() for c in self.children.values())
        return self._cached_size

    def freeze(self):
        self.frozen = True
        for c in self.children.values():
            if isinstance(c, DirectoryNode):
                c.freeze()

    def visit(
        self, predicate: Callable[[Node], bool], callback: Callable[[Node], None]
    ):
        if not predicate(self):
            return
        callback(self)
        for name, c in self.children.items():
            c.visit(predicate, callback)

    def fill_subnodes(self, tokens: Iterable[Token]):
        if self.frozen:
            raise ValueError("The tree is immutable")
        for t in tokens:
            if isinstance(t, Dir):
                self.children[t.name] = DirectoryNode(t.name, parent=self)
            elif isinstance(t, File):
                self.children[t.name] = FileNode(t.name, t.size)
            else:
                raise ValueError(f"Unknown node token: {t}")
        self.scanned = True

    def navigate_to_root(self) -> Self:
        current = self
        while current.parent:
            current = current.parent
        return current

    def navigate_to(self, relative_path: str) -> Self:
        if relative_path == "/":
            return self.navigate_to_root()
        if relative_path == "..":
            return self.parent
        # relative_path is subfolder
        if relative_path not in self.children:
            self.children[relative_path] = DirectoryNode(relative_path, parent=self)
        return self.children[relative_path]

    @classmethod
    def scan_commands(cls, tokens: list[Token]) -> Self:
        root = cls(dir_name="", parent=None)
        current = root

        command_pointer = 0
        while command_pointer < len(tokens):
            cmd_token = tokens[command_pointer]
            if not cmd_token.is_command():
                raise ValueError(f"Input token is not command: {cmd_token}")
            if isinstance(cmd_token, Ls):
                command_pointer, ls_result_tokens = _consume_ls_output(
                    tokens, command_pointer
                )
                current.fill_subnodes(ls_result_tokens)
            elif isinstance(cmd_token, Cd):
                target = cmd_token.target
                current = current.navigate_to(target)
                command_pointer += 1
            else:
                raise ValueError(f"Unknown token: {cmd_token}")
        root.freeze()
        return root

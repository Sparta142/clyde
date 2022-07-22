from dataclasses import dataclass
from typing import Callable


@dataclass
class CommandSpec:
    __slots__ = ('func',)

    func: Callable

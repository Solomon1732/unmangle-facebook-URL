#!/usr/bin/env python3


import enum
import sys
from enum import Enum
from typing import Callable, NamedTuple


class _ModeData(NamedTuple):
    """Used to hold data for different program modes."""

    prompt: str
    print_func: Callable[..., None]


def _interactive_print(*args, **kwargs) -> None:
    """Wrap a print statement with a newline before and after the statement."""

    print(file=kwargs.get("file", sys.stdout))
    print(*args, **kwargs)
    print(file=kwargs.get("file", sys.stdout))


@enum.unique
class ProgramMode(Enum):
    """Comtains defaults for different program modes."""

    QUIET = _ModeData("", print)
    INTERACTIVE = _ModeData("Enter link: ", _interactive_print)


if __name__ == "__main__":
    pass

import re
from typing import Optional, Callable


def compose_hooks(hooks: Optional[list[Callable]]) -> Callable:
    def inner(tag: str, value: str) -> str:
        for hook in hooks:
            if isinstance(hook, Callable):
                value = hook(tag, value) or value
            else:
                raise ValueError("hook's functions must be callable")
        return value

    return inner


def strip_outer_square_brackets_hook(tag: str, value: str) -> str:
    # (Square brackets used to mark the additions made by the cataloger.)
    return re.sub(rf"^\[(.*)\]\s?[{terminal_chars}]?$", r"\1", value)


def enclose_in_curly_braces_hook(tag: str, value: str) -> str:
    return f"{{{value}}}"


def escape_special_characters_hook(tag: str, value: str) -> str:
    return re.sub(rf"([&%#])", r"\\\1", value)


def use_hyphen_for_ranges_hook(tag: str, value: str) -> str:
    return re.sub(r"(\d+)-(\d+)", r"\1--\2", value)

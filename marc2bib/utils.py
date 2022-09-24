import re
from typing import Optional, Callable


def compose_hooks(hooks: Optional[list[Callable]]) -> Callable:
    def inner(tag: str, value: str) -> str:
        for hook in hooks:
            if isinstance(hook, Callable):
                new_value = hook(tag, value)
                print(new_value, "x")
                if isinstance(new_value, str):
                    value = new_value
                else:
                    raise TypeError(
                        "hook's function must return a string, "
                        f"not {value.__class__.__name__}"
                    )

            else:
                raise ValueError("hook's function must be callable")
        return value

    return inner

    
def strip_outer_square_brackets_hook(tag: str, value: str) -> str:
    # (Square brackets used to mark the additions made by the cataloger.)
    return re.sub(rf"^\[(.*)\]\s?[{terminal_chars}]?$", r"\1", value)


def enclose_in_curly_braces_hook(tag: str, value: str) -> str:
    return f"{{{value}}}"


def escape_special_characters_hook(tag: str, value: str) -> str:
    return re.sub(rf"([&%#])", r"\\\1", value)


def normalize_ranges_hook(tag: str, value: str) -> str:
    return re.sub(r"(\d+)-(\d+)", r"\1--\2", value)

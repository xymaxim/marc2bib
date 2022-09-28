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


def remove_isbd_punctuation_hook(tag: str, value: str) -> str:
    from .core import COMMON_ABBREVIATIONS

    terminal_chars = ".,:;+=/"

    value = re.sub(rf"\s([{terminal_chars}])$", "", value)

    ends_with_suffix = bool(re.search(r"[JS]r\.$", value))
    ends_with_initials = bool(re.search(r"[A-Z]\.$", value))
    ends_with_ordinal = bool(re.search(r"\d(st|nd|rd|th)\.$", value))
    ends_with_ellipsis = bool(re.search(r"\w\.{3}$", value))
    ends_with_abbrev = value.lower().endswith(COMMON_ABBREVIATIONS)

    # fmt: off
    if not (ends_with_suffix or ends_with_initials or ends_with_ordinal or
            ends_with_ellipsis or ends_with_abbrev):
        value = re.sub(fr"[{terminal_chars}]$", "", value)
    # fmt: on

    return value


def latexify_hook(tag: str, value: str) -> str:
    """Convert tag's value to make it suitable for LaTeX.

    Currently, it escapes LaTeX special characters and normalizes
    number ranges by replacing hyphens with en-dashes.
    """
    latexify = compose_hooks(
        [escape_special_characters_hook, normalize_ranges_hook]
    )
    return latexify(tag, value)


def escape_special_characters_hook(tag: str, value: str) -> str:
    return re.sub(rf"([&%#])", r"\\\1", value)


def normalize_ranges_hook(tag: str, value: str) -> str:
    return re.sub(r"(\d+)-(\d+)", r"\1--\2", value)


def strip_outer_square_brackets_hook(tag: str, value: str) -> str:
    # (Square brackets used to mark the additions made by the cataloger.)
    return re.sub(rf"^\[(.*)\]\s?[{terminal_chars}]?$", r"\1", value)


def protect_uppercase_letters_hook(tag: str, value: str) -> str:
    return re.sub(r"([A-Z]{1,})", r"{\1}", value)

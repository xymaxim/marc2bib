import re
from functools import partial
from typing import Optional, Callable


def compose_hooks(
    hooks: list[Callable[[str, str], str]],
) -> Callable[[str, str], str]:
    """Compose a group of the given hooks into a single hook.

    Hooks are applied from left to right, so that compose_hooks([f,
    g])(tag, value) is an equivalent of (g(f(tag, value)).

    This can be useful to group multiple hooks or run hooks in a row.
    """
    def inner(tag: str, value: str) -> str:
        for hook in hooks:
            if isinstance(hook, Callable):
                new_value = hook(tag, value)
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


def apply_not_for_tags(hook, tags: list[str]) -> Callable[[str, str], str]:
    """Apply a hook only for all tags except the given ones.

    Returns a tag-conditional hook wrapping a call to `hook`. As for
    excluded tags, a new hook returns the untouched tag's value.
    """
    def new_conditional_hook(tag: str, value: str) -> str:
        if tag in tags:
            return value
        else:
            return hook(tag, value)

    return new_conditional_hook


# Default hooks


def remove_isbd_punctuation_hook(
    tag: str, value: str, *, abbreviations: Optional[list[str]] = None
) -> str:
    terminal_chars = ".,:;+=/"

    value = re.sub(rf"\s([{terminal_chars}])$", "", value)

    ends_with_suffix = bool(re.search(r"[JS]r\.$", value))
    ends_with_initials = bool(re.search(r"[A-Z]\.$", value))
    ends_with_ordinal = bool(re.search(r"\d(st|nd|rd|th)\.$", value))
    ends_with_ellipsis = bool(re.search(r"\w\.{3}$", value))

    from .core import COMMON_ABBREVIATIONS

    abbreviations = abbreviations or COMMON_ABBREVIATIONS
    ends_with_abbrev = value.lower().endswith(abbreviations)

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
    if tag == "date":
        normalize_ranges_call = partial(normalize_ranges_hook, sep="/")
    else:
        normalize_ranges_call = partial(normalize_ranges_hook, sep="--")

    latexify = compose_hooks(
        [escape_special_characters_hook, normalize_ranges_call]
    )

    return latexify(tag, value)


def escape_special_characters_hook(tag: str, value: str) -> str:
    return re.sub(rf"([&%#])", r"\\\1", value)


def normalize_ranges_hook(tag: str, value: str, *, sep: str = "--") -> str:
    return re.sub(r"(\d+)-(\d+)", rf"\1{sep}\2", value)


# Pre-defined hooks


def strip_outer_square_brackets_hook(tag: str, value: str) -> str:
    # (Square brackets used to mark the additions made by the cataloger.)
    return re.sub(rf"^\[(.*)\]\s?[{terminal_chars}]?$", r"\1", value)


def protect_uppercase_letters_hook(tag: str, value: str) -> str:
    return re.sub(r"([A-Z]{1,})", r"{\1}", value)

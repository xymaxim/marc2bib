"""This is a main marc2bib package file. 

Make sure to check out the FAQ [1] for the MARC 21 at the Library of
Congress (LOC) website. There is a lot information located on the main
page [2] -- but first, take a look at a brief description and a summary
of the MARC 21 fields [3]. While hacking on this package, you may also
find useful both the full and concise versions of the "MARC 21 Format
for Bibliographic Data" document [4]. Information regarding the BibTeX
entry types and corresponding fields can be found in Section 3 of the
original manual dated 1988 [5].

[1] http://www.loc.gov/marc/faq.html
[2] http://www.loc.gov/marc/
[3] http://www.loc.gov/marc/umb/
[4] http://www.loc.gov/marc/bibliographic/
[5] http://ctan.uni-altai.ru/biblio/bibtex/base/btxdoc.pdf
"""

import re
import warnings
from typing import Callable, Dict, Iterable, Optional, Union

from pymarc import MARCReader, Record  # type: ignore

from . import tagfuncs as default_tagfuncs
from .utils import (
    compose_hooks,
    escape_special_characters_hook,
    normalize_ranges_hook,
)


# By default, book entry may contain either one of author or editor
# fields. See convert function to know how they are treated,
# especially in case if both fields are requested.
BOOK_REQ_TAGFUNCS = {
    "author": default_tagfuncs.get_author,
    "editor": default_tagfuncs.get_editor,
    "publisher": default_tagfuncs.get_publisher,
    "title": default_tagfuncs.get_title,
    "year": default_tagfuncs.get_year,
}

BOOK_OPT_TAGFUNCS = {
    "address": default_tagfuncs.get_address,
    "edition": default_tagfuncs.get_edition,
    "volume": default_tagfuncs.get_volume,
    "volumes": default_tagfuncs.get_volumes,
    "note": default_tagfuncs.get_note,
    "number": default_tagfuncs.get_volume,
    "pages": default_tagfuncs.get_pages,
    "series": default_tagfuncs.get_series,
    "subtitle": default_tagfuncs.get_subtitle,
    "isbn": Record.isbn,
}


class MARC2BibError(Exception):
    pass


# fmt: off
COMMON_ABBREVIATIONS = (
    "co.", "ed.", "eds.", "et al.", "v.", "vol.", "vols.", "inc.", "p.",
)
# fmt: on


def remove_isbd_punctuation(s: str) -> str:
    terminal_chars = ".,:;+=/"

    s = re.sub(rf"\s([{terminal_chars}])$", "", s)

    ends_with_suffix = bool(re.search(r"[JS]r\.$", s))
    ends_with_initials = bool(re.search(r"[A-Z]\.$", s))
    ends_with_ordinal = bool(re.search(r"\d(st|nd|rd|th)\.$", s))
    ends_with_ellipsis = bool(re.search(r"\w\.{3}$", s))
    ends_with_abbrev = s.lower().endswith(COMMON_ABBREVIATIONS)

    # fmt: off
    if not (ends_with_suffix or ends_with_initials or ends_with_ordinal or
            ends_with_ellipsis or ends_with_abbrev):
        s = re.sub(fr"[{terminal_chars}]$", "", s)
    # fmt: on

    return s


def latexify_hook(tag: str, value: str) -> str:
    """Convert tag's value to make it suitable for LaTeX.

    Currently, it escapes LaTeX special characters and normalizes
    number ranges by replacing hyphens with en-dashes.
    """
    latexify = compose_hooks(
        [escape_special_characters_hook, normalize_ranges_hook]
    )
    return latexify(tag, value)


def _as_bibtex(
    bibtype: str,
    bibkey: str,
    tags: Dict[str, str],
    indent: int,
    do_align: bool,
) -> str:
    tag_width = max(map(len, tags)) if do_align else 0

    bibtex = f"@{bibtype}{{{bibkey}"
    for tag, value in sorted(tags.items()):
        bibtex += f',\n{" " * indent}{tag:<{tag_width}} = {{{value}}}'
    bibtex += "\n}\n"

    return bibtex


TagfunctionsSig = Dict[str, Callable[[Record], str]]
PostHookSig = Callable[[str, str], str]


def map_tags(
    record: Record,
    tagfuncs: Optional[TagfunctionsSig] = None,
    include: Union[str, Iterable[str]] = "required",
    allow_blank: bool = False,
    remove_punctuation: bool = True,
    latexify: bool = True,
    post_hooks: Optional[list[PostHookSig]] = None,
    version: str = "bibtex",
) -> Dict[str, str]:
    """Map MARC fields of a record into the BibTeX tags.

    See docstring of :obj:`marc2bib.convert()` for the arguments.
    """
    ctx_tagfuncs = BOOK_REQ_TAGFUNCS.copy()
    if version == "biblatex":
        ctx_tagfuncs["location"] = ctx_tagfuncs.pop("address")

    if include == "all":
        ctx_tagfuncs.update(BOOK_OPT_TAGFUNCS)
    elif include != "required":
        # Check if `include` argument is iterable and not a string.
        # We are no longer interested in a string because all
        # possible values are already passed.
        try:
            assert not isinstance(include, str)
            iter(include)
        except (AssertionError, TypeError) as e:
            msg = (
                "include argument should be an iterable or one of "
                f"('required', 'all'), got {include}"
            )
            e.args += (msg,)
            raise ValueError(e)
        else:
            # Ensure that all of the user-provided tags has a
            # tag-function defined by default in optional tags.
            if not all(tag in BOOK_OPT_TAGFUNCS for tag in include):
                raise ValueError(
                    "include argument contains unknown optional tag(s)"
                )
            for tag in include:
                ctx_tagfuncs[tag] = BOOK_OPT_TAGFUNCS[tag]

    if tagfuncs:
        ctx_tagfuncs.update(tagfuncs)

    ctx_tags = {}

    # Check for author field first, then editor.
    author = ctx_tagfuncs["author"](record)
    if author:
        # Editor field can be requested along with author.
        if "editor" not in include or "editor" not in tagfuncs:
            ctx_tagfuncs.pop("editor")
    else:
        editor = ctx_tagfuncs["editor"](record)
        if editor is None:
            msg = "both author and editor (required) tags are treated empty."
            raise MARC2BibError(msg)
        else:
            ctx_tagfuncs.pop("author")

    for tag, func in ctx_tagfuncs.items():
        tag_value = func(record)
        if not isinstance(tag_value, str) and tag_value is not None:
            msg = (
                f"Returned value from {func} for {tag} tag "
                "should be a string or None"
            )
            raise TypeError(msg)

        if tag_value is None:
            msg = (
                f"The content of tag `{tag}` is None, "
                "replacing it with an empty value"
            )
            warnings.warn(UserWarning(msg))
            tag_value = ""

        if remove_punctuation:
            tag_value = remove_isbd_punctuation(tag_value)

        if post_hooks:
            composed = compose_hooks(post_hooks)
            tag_value = composed(tag, tag_value)

        blank_and_allowed = tag_value.strip() == "" and allow_blank
        if tag_value.strip() or blank_and_allowed:
            # Abover all, we only accept non-blank field values and
            # empty values if they are allowed by the given argument.
            ctx_tags[tag] = tag_value

    return ctx_tags


def tags_to_bibtex(
    tags: Dict[str, str],
    bibtype: str = "book",
    bibkey: Optional[Union[str, Callable[[Record], str]]] = None,
    indent: int = 1,
    do_align: bool = False,
) -> str:
    """Translate BibTeX tags into a BibTeX-formatted string.

    See docstring of :obj:`marc2bib.convert()'` for the arguments.
    """
    if bibkey is None:
        try:
            authors_or_editors = tags["author"]
        except KeyError:
            authors_or_editors = tags["editor"]
        surname = authors_or_editors.split(",")[0]
        bibkey_value = surname.lower() + tags["year"]
    elif callable(bibkey):
        bibkey_value = bibkey(tags)
    else:
        bibkey_value = bibkey

    bibtex = _as_bibtex(bibtype, bibkey_value, tags, indent, do_align)

    return bibtex


def convert(
    record: Record,
    bibtype: str = "book",
    bibkey: Optional[Union[str, Callable[[Record], str]]] = None,
    tagfuncs: Optional[TagfunctionsSig] = None,
    include: Union[str, Iterable[str]] = "required",
    allow_blank: bool = False,
    remove_punctuation: bool = True,
    latexify: bool = True,
    post_hooks: Optional[list[PostHookSig]] = None,
    indent: int = 1,
    do_align: bool = False,
) -> str:
    """Converts an instance of :class:`pymarc.Record` to a BibTeX entry.

    By default all defined (required and optional) fields (tags) for
    book entry are returned. Use ``tagfuncs`` argument to extend or
    override returned tags. If you want to control the returned tags,
    use ``include`` argument instead.

    Args:
        record: An instance of :class:`pymarc.Record`.
        bibtype: A BibTeX entry type. Currently only
            book entries are fully supported.
        bibkey: A BibTeX citation key. If ``None``, then the
            author-date style is used, e.g. "author2022". If the
            author is not provided, then the first editor will be
            used. Accepts callable with a Record as an argument.
        tagfuncs: A dictionary of functions used to
            retrieve a BibTeX tag content. The key of the dictionary
            is the name of a particular tag. Your function (we call
            this tag-function) must take one argument, a reference to
            the given record, and return a string. Example usage::

            def tagfunc(record: pymarc.Record) -> str:
                # Insert your way to get the field value here.
                ...
            convert(record, tagfuncs={'tag': tagfunc})
        include: Defaults to 'required'. The value can be either
            * 'all' -- include all defined tags for the given ``bibtype``
            * 'required' -- include only required tags for the given
                            ``bibtype``
            * a list of tags to include together with the required
              ones. For example, ['edition'].
        allow_blank (bool): If True, also include tags with a blank
            content (empty or contains only whitespace characters)
            to the output. Defaults to False.
        remove_punctuation (bool): If True, remove ending ISBD
            punctuation. Defaults to True.
        latexify (bool): If True, convert tag's content for use with
            LaTeX. Defaults to True.
        indent (int): The tag line indentation. Defaults to 1.
        do_align: If True, align tag values by the longest tag.
            Defaults to False.

    Returns:
        A BibTeX-formatted string.

    """
    ctx_tags = map_tags(
        record,
        tagfuncs,
        include,
        allow_blank,
        remove_punctuation,
        latexify,
        post_hooks,
    )
    bibtex = tags_to_bibtex(ctx_tags, bibtype, bibkey, indent, do_align)

    return bibtex

"""Here are all currently defined tag-functions."""

import re
from typing import Optional

from pymarc import Record  # type: ignore


def get_address(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd25x28x.html
    fields = record.get_fields("260", "264")
    if fields:
        field = fields[0]
        return field["a"].replace("[", "").replace("]", "").rstrip(": ")
    else:
        return None


def get_author(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd1xx.html
    # https://www.loc.gov/marc/bibliographic/bd400.html
    # https://www.loc.gov/marc/bibliographic/bd600.html
    # https://www.loc.gov/marc/bibliographic/bd800.html
    fields = record.get_fields("100", "110", "400", "600", "800")
    if fields:
        field = fields[0]
        # In this case the subfield value is a pronoun
        if field.tag == "400" and field.indicator2 == "1":
            rv = None
        else:
            rv = field["a"]
        return rv
    else:
        return None


def get_edition(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd250.html
    field = record["250"]
    if field:
        return field["a"]
    else:
        return None


def get_editor(record: Record) -> Optional[str]:
    editors = []

    fields = record.get_fields("700")
    for field in fields:
        editor = field["a"]
        ends_with_initials = bool(re.search(r"[A-Z]\.$", editor))
        if not ends_with_initials:
            editors.append(editor.rstrip(".,"))
        else:
            editors.append(editor)

    if editors:
        return " and ".join(editors)
    else:
        return None


def get_publisher(record: Record) -> Optional[str]:
    return record.publisher()


def get_title(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd245.html
    field = record["245"]
    try:
        return field["a"]
    except TypeError:
        return None


def get_subtitle(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd245.html
    field = record["245"]
    if field:
        return field["b"]
    else:
        return None


def get_year(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd25x28x.html
    year = record.pubyear()
    if year:
        return year.lstrip("c")
    else:
        return None


def get_volume(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd300.html
    field = record["300"]

    as_roman_numeral_re = r"^\[?([mdclxvi]+)\]?,"
    with_abbrev_re = r"v\.\s([0-9]+)"

    if field:
        volume_number_pa = re.compile(
            r"|".join((as_roman_numeral_re, with_abbrev_re))
        )
        m = volume_number_pa.search(field["a"])
        return m.group(1) or m.group(2)
    else:
        return None


def get_volumes(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd300.html
    field = record["300"]
    if field:
        m = re.search(r"([0-9]+)\s[v\s.|volumes]", field["a"])
        return m.group(1) if m else None
    else:
        return None


def get_pages(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd300.html
    field = record["300"]
    if field:
        m = re.search(r"\[?(([0-9]+-)?[0-9]+)\]?\s?p\.?", field["a"])
        return m.group(1) if m else None
    else:
        return None


def get_note(record: Record) -> Optional[str]:
    raise NotImplementedError


def get_series(record: Record) -> Optional[str]:
    # https://www.loc.gov/marc/bibliographic/bd490.html
    field = record["490"]
    if field:
        return field["a"].rstrip(",")
    else:
        return None

import pytest
from pymarc import MARCReader

from marc2bib import map_tags


def test_nlm_record_set():
    removed = "tests/validation/TestBibsWithIsbdPunctuationRemoved.mrc"
    original = "tests/validation/TestBibsWithIsbdPunctuation.mrc"

    with open(removed, "rb") as fr, open(original, "rb") as fo:
        reader_removed = MARCReader(fr)
        for record_removed in reader_removed:
            cn = record_removed["001"].value()
            # We are interested in book-like records with ISBN
            # values. Also, the records listed below don't have author
            # or editor fields (only field 710).
            if not record_removed.isbn() or cn in (
                "603149",
                "603235",
                "603253",
                "1627172",
            ):
                continue

            reader_original = MARCReader(fo)
            for record_original in reader_original:
                if cn == record_original["001"].value():
                    tags_removed = map_tags(
                        record_removed,
                        allow_blank=True,
                        remove_punctuation=False,
                    )
                    tags_original = map_tags(
                        record_original,
                        allow_blank=True,
                        remove_punctuation=True,
                    )

                    assert tags_removed["title"] == tags_original["title"]
                    assert tags_removed["year"] == tags_original["year"]
                    assert (
                        tags_removed["publisher"] == tags_original["publisher"]
                    )

                    break

            fo.seek(0)

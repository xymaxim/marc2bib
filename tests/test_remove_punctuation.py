import pytest
from marc2bib import remove_isbd_punctuation_hook


def test_terminal_space_and_punctuation():
    assert "Test" == remove_isbd_punctuation_hook("", "Test .")
    assert "Test" == remove_isbd_punctuation_hook("", "Test ,")
    assert "Test" == remove_isbd_punctuation_hook("", "Test :")
    assert "Test" == remove_isbd_punctuation_hook("", "Test ;")
    assert "Test" == remove_isbd_punctuation_hook("", "Test +")
    assert "Test" == remove_isbd_punctuation_hook("", "Test /")
    assert "Test" == remove_isbd_punctuation_hook("", "Test =")


def test_punctuation_without_space():
    assert "Test" == remove_isbd_punctuation_hook("", "Test.")


def test_year():
    assert "2022" == remove_isbd_punctuation_hook("", "2022.")


def test_initials():
    assert "A.B." == remove_isbd_punctuation_hook("", "A.B.")
    assert "A.B." == remove_isbd_punctuation_hook("", "A.B.,")


def test_name_suffixes():
    assert "Jane Doe, Sr." == remove_isbd_punctuation_hook("", "Jane Doe, Sr.")
    assert "John Doe, Jr." == remove_isbd_punctuation_hook("", "John Doe, Jr.")


def test_ellipsis():
    assert "Test..." == remove_isbd_punctuation_hook("", "Test...")


def test_ordinal_numbers():
    assert "1st." == remove_isbd_punctuation_hook("", "1st.")
    assert "2nd." == remove_isbd_punctuation_hook("", "2nd.")
    assert "3rd." == remove_isbd_punctuation_hook("", "3rd.")
    assert "4th." == remove_isbd_punctuation_hook("", "4th.")


@pytest.mark.skipif()
def test_strip_outer_square_brackets():
    assert "Test" == remove_isbd_punctuation_hook("", "[Test]")
    assert "Test" == remove_isbd_punctuation_hook("", "[Test].")
    assert "One, [two]" == remove_isbd_punctuation_hook("", "[One, [two]]")


@pytest.mark.skipif()
def test_strip_outer_square_brackets():
    assert "Test" == remove_isbd_punctuation_hook("", "[Test]")
    assert "Test" == remove_isbd_punctuation_hook("", "[Test].")
    assert "Test" == remove_isbd_punctuation_hook("", "[Test] ;")
    assert "Another [one]" == remove_isbd_punctuation_hook("", "Another [one]")


def test_common_abbreviation():
    assert "ed." == remove_isbd_punctuation_hook("", "ed.")


def test_common_abbreviation_capitalized():
    assert "Co." == remove_isbd_punctuation_hook("", "Co.")

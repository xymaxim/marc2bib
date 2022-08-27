import pytest
from marc2bib import convert
from marc2bib.tagfuncs import get_volume, get_volumes, get_pages


def test_required_book_tags(rec_hargittai):
    bibtex = (
        "@book{hargittai2009,\n"
        " author = {Hargittai, Magdolna},\n"
        " publisher = {Springer},\n"
        " title = {Symmetry through the eyes of a chemist},\n"
        " year = {2009}\n"
        "}\n"
    )
    assert convert(rec_hargittai, include="required") == bibtex


def test_custom_bibtype(rec_hargittai):
    output = convert(rec_hargittai, bibtype="BOOK")
    assert "@BOOK{" in output


def test_custom_tagfuncs(rec_hargittai):
    custom_tagfuncs = dict(title=lambda _: "Test")
    output = convert(rec_hargittai, tagfuncs=custom_tagfuncs)
    assert "title = {Test}" in output


def test_extend_tagfuncs(rec_hargittai):
    new_tagfuncs = dict(new=lambda _: "Test")
    output = convert(rec_hargittai, tagfuncs=new_tagfuncs)
    assert "new = {Test},\n" in output


def test_new_bibkey(rec_hargittai):
    output = convert(rec_hargittai, bibkey="hargittai2009-sym")
    assert "hargittai2009-sym" in output


def test_also_include_edition_field(rec_hargittai):
    output = convert(rec_hargittai, include=["edition"])
    assert "edition = {3rd ed.},\n" in output


def test_another_publication_field(rec_tsing):
    bibtex = convert(rec_tsing, include=["address"])
    assert "address = {Princeton}" in bibtex
    assert "publisher = {Princeton University Press}" in bibtex


def test_subtitle(rec_tsing):
    output = convert(rec_tsing, include=["subtitle"])
    assert "title = {The mushroom at the end of the world}" in output
    assert (
        "subtitle = {on the possibility of life in capitalist ruins}" in output
    )


def test_volume(rec_sholokhov):
    output = convert(rec_sholokhov, include=["volumes"])
    assert "volumes = {4}" in output


def test_series(rec_clusters):
    output = convert(rec_clusters, include=["series"])
    assert "series = {Cluster physics}" in output


def test_get_pages_abbreviated():
    assert "123" == get_pages({"300": {"a": "123p."}})
    assert "123" == get_pages({"300": {"a": "123 p."}})
    assert "123" == get_pages({"300": {"a": "123 p"}})

    
def test_get_pages_non_abbreviated():
    assert "123" == get_pages({"300": {"a": "123 pages"}})

    
def test_get_pages_in_brackets():
    assert "123" == get_pages({"300": {"a": "[123] pages"}})

    
def test_get_range_of_pages():
    assert "123-133" == get_pages({"300": {"a": "123-133 p."}})

    
def test_get_volume_in_arabic_numerals():
    assert "1" == get_volume({"300": {"a": "v. 1"}})

    
def test_get_volume_in_roman_numerals():
    assert "i" == get_volume({"300": {"a": "i,"}})
    assert "xv" == get_volume({"300": {"a": "xv,"}})
    assert "mdclxvi" == get_volume({"300": {"a": "mdclxvi,"}})

    
def test_get_volume_in_roman_numerals_with_brackets():
    assert "ii" == get_volume({"300": {"a": "[ii],"}})

    
def test_get_volumes_abbreviated():
    assert "2" == get_volumes({"300": {"a": "2 v."}})

    
def test_get_volumes_non_abbreviated():
    assert "2" == get_volumes({"300": {"a": "2 volumes"}})

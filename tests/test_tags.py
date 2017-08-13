import pytest
from marc2bib import convert


def test_required_book_tags(rec_hargittai):
    bibtex = ("@book{hargittai2009,\n"
              " author = {Hargittai, István},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")
    assert convert(rec_hargittai, include='required') == bibtex

def test_custom_bibtype(rec_hargittai):
    output = convert(rec_hargittai, bibtype='BOOK')
    assert '@BOOK{' in output

def test_custom_tagfuncs(rec_hargittai):
    custom_tagfuncs = dict(title=lambda _: 'Meow')
    output = convert(rec_hargittai, tagfuncs=custom_tagfuncs)
    assert ' title = {Meow}' in output

def test_extend_tagfuncs(rec_hargittai):
    new_tagfuncs = dict(new=lambda _: 'Meow')
    output = convert(rec_hargittai, tagfuncs=new_tagfuncs)
    assert ' new = {Meow},\n' in output

def test_new_bibkey(rec_hargittai):
    output = convert(rec_hargittai, bibkey='hargittai2009-sym')
    assert 'hargittai2009-sym' in output

def test_also_include_edition_field(rec_hargittai):
    output = convert(rec_hargittai, include=['edition'])
    assert ' edition = {3rd ed.},\n' in output

def test_another_publication_field(rec_tsing):
    bibtex = convert(rec_tsing, include=['address'])
    assert ' address = {Princeton}' in bibtex
    assert ' publisher = {Princeton University Press}' in bibtex

def test_subtitle(rec_tsing):
    output = convert(rec_tsing)
    assert 'The mushroom at the end of the world: on the possibility of life in capitalist ruins' in output

def test_volume(rec_sholokhov):
    output = convert(rec_sholokhov, include=['volume'])
    assert ' volume = {4 v.}' in output

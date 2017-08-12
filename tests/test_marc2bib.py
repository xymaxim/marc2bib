import pytest
from pymarc import MARCReader

from marc2bib import convert


@pytest.fixture(scope='function')
def rec_hargittai(request):
    # This MARC file has been downloaded from
    # http://pi.lib.uchicago.edu/1001/cat/bib/8888814
    reader = MARCReader(open('tests/hargittai2009.mrc', 'rb'))
    request.addfinalizer(reader.close)
    return next(reader)

@pytest.fixture(scope='function')
def rec_tsing(request):
    # This MARC file has been downloaded from
    # https://lccn.loc.gov/2014037624
    reader = MARCReader(open('tests/tsing2015.mrc', 'rb'))
    request.addfinalizer(reader.close)
    return next(reader)


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
    assert '@BOOK{' in  output

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

def test_not_str_tagfunc_return(rec_hargittai):
    def yay_func(_): return None

    with pytest.raises(TypeError) as excinfo:
        convert(rec_hargittai, tagfuncs={'yay': yay_func})

    assert ('yay_func' and 'yay') in str(excinfo.value)

def test_include_only_required_fields(rec_hargittai):
    bibtex = ("@book{hargittai2009,\n"
              " author = {Hargittai, István},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, include='required') == bibtex
    
def test_different_indent(rec_hargittai):
    bibtex = ("@book{hargittai2009,\n"
              "  author = {Hargittai, István},\n"
              "  publisher = {Springer},\n"
              "  title = {Symmetry through the eyes of a chemist},\n"
              "  year = {2009}\n"
              "}\n")
    output = convert(rec_hargittai, indent=2, include='required')
    assert output == bibtex

def test_also_include_edition_field(rec_hargittai):
    output = convert(rec_hargittai, include=['edition'])
    assert ' edition = {3rd ed.},\n' in output

def test_custom_tagfuncs_priority_over_include(rec_hargittai):
    custom_tagfuncs = dict(tag=lambda _: 'Meow')
    output = convert(rec_hargittai, tagfuncs=custom_tagfuncs, include='required')
    assert ' tag = {Meow},\n' in output

def test_invalid_include_should_raises(rec_hargittai):
    with pytest.raises(TypeError):
        convert(rec_hargittai, include=None)

def test_unknown_include_string(rec_hargittai):
    with pytest.raises(AssertionError):
        convert(rec_hargittai, include='unknown')

def test_include_with_non_existent_tag(rec_hargittai):
    with pytest.raises(ValueError):
        convert(rec_hargittai, include=['non-existent'])

def test_another_publication_field(rec_tsing):
    bibtex = convert(rec_tsing)
    assert ' address = {Princeton}' in bibtex
    assert ' publisher = {Princeton University Press}' in bibtex

def test_subtitle(rec_tsing):
    output = convert(rec_tsing)
    assert 'The mushroom at the end of the world: on the possibility of life in capitalist ruins' in output

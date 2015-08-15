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
def rec_lundqvist(request):
    # This MARC file has been downloaded from
    # http://pi.lib.uchicago.edu/1001/cat/bib/795566
    reader = MARCReader(open('tests/lundqvist1983.mrc', 'rb'))
    request.addfinalizer(reader.close)
    return next(reader)


def test_default_book_tagfuncs(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " address = {Dordrecht},\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai) == bibtex

def test_custom_bibtype(rec_hargittai):
    bibtex = ("@BOOK{Hargittai2009,\n"
              " address = {Dordrecht},\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, bibtype='BOOK') == bibtex

def test_custom_tagfuncs(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " address = {Dordrecht},\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Meow.},\n" # Rawr!
              " year = {2009}\n"
              "}\n")

    custom_tagfuncs = dict(title=lambda _: 'Meow.')
    assert convert(rec_hargittai, tagfuncs=custom_tagfuncs) == bibtex

def test_extend_tagfuncs(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " address = {Dordrecht},\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              # Meet url, a new entry tag.
              " url = {http://dx.doi.org/10.1007/978-1-4020-5628-4},\n"
              " year = {2009}\n"
              "}\n")

    new_tagfuncs = dict(url=lambda x: x['856']['u'])
    assert convert(rec_hargittai, tagfuncs=new_tagfuncs) == bibtex

def test_new_bibkey(rec_hargittai):
    bibtex = ("@book{Hargittai2009Symmetry,\n"
              " address = {Dordrecht},\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, bibkey='Hargittai2009Symmetry') == bibtex

def test_not_str_tagfunc_return(rec_hargittai):
    def yay_func(_): return None

    with pytest.raises(TypeError) as excinfo:
        convert(rec_hargittai, tagfuncs={'yay': yay_func})

    assert ('yay_func' and 'yay') in str(excinfo.value)

def test_different_indent(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              "  address = {Dordrecht},\n"
              "  author = {Hargittai, István},\n"
              "  edition = {3rd ed.},\n"
              "  publisher = {Springer},\n"
              "  title = {Symmetry through the eyes of a chemist},\n"
              "  year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, indent=2) == bibtex

def test_include_only_required_fields(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " author = {Hargittai, István},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, include='required') == bibtex

def test_also_include_edition_fields(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, include=['edition']) == bibtex

def test_include_both_required_and_additional_fields(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " address = {Dordrecht},\n"
              " author = {Hargittai, István},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai) == bibtex
    assert convert(rec_hargittai, include='all') == bibtex

def test_custom_tagfuncs_priority_over_include(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
              " author = {Hargittai, István},\n"
              " publisher = {Springer},\n"
              " tag = {value},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    custom_tagfuncs = dict(tag=lambda _: 'value')
    rv = convert(rec_hargittai, tagfuncs=custom_tagfuncs, include='required')
    assert rv == bibtex

def test_invalid_include_should_raises(rec_hargittai):
    with pytest.raises(TypeError):
        convert(rec_hargittai, include=None)

def test_unknown_include_string(rec_hargittai):
    with pytest.raises(AssertionError):
        convert(rec_hargittai, include='unknown')

def test_include_with_non_existent_tag(rec_hargittai):
    with pytest.raises(ValueError):
        convert(rec_hargittai, include=['non-existent'])

def test_only_editors(rec_lundqvist):
    bibtex = ("@book{Lundqvist1983,\n"
              " editor = {Lundqvist, Stig and March, Norman H.},\n"
              " publisher = {Plenum Press},\n"
              " title = {Theory of the inhomogeneous electron gas },\n"
              " year = {1983}\n"
              "}\n")

    assert convert(rec_lundqvist, include='required') == bibtex

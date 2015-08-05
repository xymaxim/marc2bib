import pytest
from pymarc import MARCReader

from marc2bib import convert


@pytest.fixture(scope='function')
def rec_hargittai(request):
    # This MARC file has been downloaded from
    # http://pi.lib.uchicago.edu/1001/cat/bib/8888814
    reader = MARCReader(open('tests/hargittai2009.mrc', 'rb'),
                        to_unicode=True, force_utf8=True)
    request.addfinalizer(reader.close)
    return next(reader)


def test_default_book_tagfuncs(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " publisher = {Springer},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            " year = {2009}\n"
            "}\n")

    assert convert(rec_hargittai) == bibtex

def test_custom_bibtype(rec_hargittai):
    bibtex = ("@BOOK{Hargittai2009,\n"
              " author = {I. Hargittai, M. Hargittai},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    assert convert(rec_hargittai, bibtype='BOOK') == bibtex

def test_custom_tagfuncs(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " publisher = {Springer},\n"
            " title = {Meow.},\n" # Rawr!
            " year = {2009}\n"
            "}\n")

    custom_tagfuncs = dict(title=lambda _: 'Meow.')
    assert convert(rec_hargittai, tagfuncs=custom_tagfuncs) == bibtex

def test_extend_tagfuncs(rec_hargittai):
    bibtex = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
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
            " author = {I. Hargittai, M. Hargittai},\n"
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

    excmsg = str(excinfo.value)
    assert ('yay_func' and 'yay') in excmsg

import pytest
from pymarc import MARCReader

from marc2bib import convert


@pytest.fixture(scope='function')
def hargittai_reader(request):
    reader = MARCReader(open('tests/hargittai2009.mrc', 'rb'),
                        to_unicode=True, force_utf8=True)
    def fin():
        reader.close()
    request.addfinalizer(fin)
    return reader


def test_default_book_tagfuncs(hargittai_reader):
    bibtex = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " publisher = {Springer},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            " year = {2009}\n"
            "}\n")

    rec = next(hargittai_reader)
    assert convert(rec) == bibtex

def test_custom_bibtype(hargittai_reader):
    bibtex = ("@BOOK{Hargittai2009,\n"
              " author = {I. Hargittai, M. Hargittai},\n"
              " edition = {3rd ed.},\n"
              " publisher = {Springer},\n"
              " title = {Symmetry through the eyes of a chemist},\n"
              " year = {2009}\n"
              "}\n")

    rec = next(hargittai_reader)
    assert convert(rec, bibtype='BOOK') == bibtex

def test_custom_tagfuncs(hargittai_reader):
    bibtex = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " publisher = {Springer},\n"
            " title = {Meow.},\n" # Rawr!
            " year = {2009}\n"
            "}\n")

    rec = next(hargittai_reader)
    custom_tagfuncs = dict(title=lambda _: 'Meow.')
    assert convert(rec, tagfuncs=custom_tagfuncs) == bibtex

def test_extend_tagfuncs(hargittai_reader):
    bibtex = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " publisher = {Springer},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            # Meet url, a new entry tag.
            " url = {http://dx.doi.org/10.1007/978-1-4020-5628-4},\n"
            " year = {2009}\n"
            "}\n")

    rec = next(hargittai_reader)
    new_tagfuncs = dict(url=lambda x: x['856']['u'])
    assert convert(rec, tagfuncs=new_tagfuncs) == bibtex

def test_new_bibkey(hargittai_reader):
    bibtex = ("@book{Hargittai2009Symmetry,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " publisher = {Springer},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            " year = {2009}\n"
            "}\n")

    rec = next(hargittai_reader)
    assert convert(rec, bibkey='Hargittai2009Symmetry') == bibtex

def test_not_str_tagfunc_return(hargittai_reader):
    rec = next(hargittai_reader)
    def yay_func(_): return None
    with pytest.raises(TypeError) as excinfo:
        convert(rec, tagfuncs={'yay': yay_func})
    excmsg = str(excinfo.value)
    assert ('yay_func' and 'yay') in excmsg

import pytest
from marc2bib import convert


def test_not_str_tagfunc_return(rec_hargittai):
    def yay_func(_): return 6.626
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

def test_tag_values_alignment(rec_hargittai):
    bibtex = ("@book{hargittai2009,\n"
              " author    = {Hargittai, István},\n"
              " publisher = {Springer},\n"
              " title     = {Symmetry through the eyes of a chemist},\n"
              " year      = {2009}\n"
              "}\n")
    assert convert(rec_hargittai, include='required', align=True) == bibtex
    
def test_tag_with_none_value(rec_sholokhov):
    none_func = lambda _: None
    with pytest.warns(UserWarning):
        output = convert(rec_sholokhov, tagfuncs=dict(note=none_func))
        assert ' none = {None}' not in output

def test_disallow_blank_tags_by_default(rec_sholokhov):
    tagfuncs = {
        'firstblank': lambda _: '',
        'secondblank': lambda _: ' ', 
    }
    output = convert(rec_sholokhov, tagfuncs=tagfuncs)
    assert ' firstblank = {}' not in output
    assert ' secondblank =' not in output

def test_allow_blank_tags(rec_sholokhov):
    tagfuncs = {
        'firstblank': lambda _: '',
        'secondblank': lambda _: ' ', 
    }
    output = convert(rec_sholokhov, tagfuncs=tagfuncs, allow_blank=True)
    assert ' firstblank = {}' in output
    assert ' secondblank = { }' in output

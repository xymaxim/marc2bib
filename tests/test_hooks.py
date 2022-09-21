import pytest
from marc2bib import convert
from marc2bib.core import latexify_hook
from marc2bib.utils import *


def test_compose_hooks():
    append = lambda _, x: x + x
    multiply = lambda _, x: x * 2
    assert "aaaa" == compose_hooks([append, multiply])("", "a")


def test_compose_hooks_with_null_hook():
    append = lambda _, x: x + x
    null = lambda _, x: None
    assert "aa" == compose_hooks([append, null])("", "a")


def test_compose_hooks_should_raise_value_error():
    with pytest.raises(ValueError):
        compose_hooks([None])("", "")


class TestHookFunctions:
    def test_enclose_in_curly_braces_hook(self):
        assert "{Test}" == enclose_in_curly_braces_hook("", "Test")

    def test_escape_special_characters(self):
        assert r"A \& B" == escape_special_characters_hook("", "A & B")

    def test_use_hyphen_for_ranges_hook(self):
        assert "12--34" == use_hyphen_for_ranges_hook("", "12-34")

    def test_latexify_hook(self):
        assert r"A \& B, 12--34" == latexify_hook("", "A & B, 12-34")


class TestHooksOnRecords:
    def test_conditional_post_hook(self, rec_tsing):
        def hook(tag, value):
            if tag == "title":
                return f"{{{value}}}"

        output = convert(rec_tsing, post_hooks=[hook])
        assert "title = {{The mushroom at the end of the world}}" in output
        assert "author = {Tsing, Anna Lowenhaupt}" in output

    def test_two_post_hooks(self, rec_tsing):
        def hook1(tag, value):
            return f"{value}."

        def hook2(tag, value):
            return f"{{{value}}}"

        output = convert(rec_tsing, post_hooks=[hook1, hook2])
        assert "title = {{The mushroom at the end of the world.}}" in output

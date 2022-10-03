import pytest
from marc2bib import convert
from marc2bib.hooks import *


def test_compose_hooks():
    append = lambda _, v: v + v
    multiply = lambda _, v: v * 2
    assert "aaaa" == compose_hooks([append, multiply])("tag", "a")


def test_compose_hooks_with_null_hook():
    with pytest.raises(TypeError):
        compose_hooks([lambda t, v: None])("tag", "value")


def test_compose_hooks_with_non_callable_hook():
    with pytest.raises(ValueError):
        compose_hooks([None])("tag", "value")


def test_apply_hook_not_for_tags():
    hook = apply_hook_not_for_tags(lambda t, v: "Not test", ["test"])
    assert "Not test" == hook("tag", "Test")
    assert "Test" == hook("test", "Test")


class TestHookFunctions:
    def test_protect_uppercase_letters_hook(self):
        assert "{A}b {AB}" == protect_uppercase_letters_hook("tag", "Ab AB")

    def test_escape_special_characters(self):
        assert r"A \& B" == escape_special_characters_hook("tag", "A & B")

    def test_normalize_ranges_hook(self):
        assert "12--34" == normalize_ranges_hook("tag", "12-34")

    def test_latexify_hook(self):
        assert r"A \& B, 12--34" == latexify_hook("tag", "A & B, 12-34")


class TestHooksOnRecords:
    def test_conditional_post_hook(self, rec_tsing):
        def hook(tag, value):
            return f"{{{value}}}" if tag == "title" else value

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

    def test_default_latexify_post_hook(self, rec_tsing):
        tagfuncs = {"test": lambda x: "12-23"}
        output = convert(rec_tsing, tagfuncs=tagfuncs)
        assert "test = {12--23}" in output

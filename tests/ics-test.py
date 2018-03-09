"""Tests for Functions from core for part-like strings."""

from datasimple.core import comppart


def comppart_test():
    assert '' == comppart(''), 'empty string'
    assert '' == comppart(' \r \n \t '), 'whitespace'
    assert 'HELL0W0RLD' == comppart(' hello-world '), 'simple with ohs'
    assert 'PART' == comppart(' the part '), 'the prefix'
    assert 'A' == comppart(r"""A~!@#$%^&*()_=+{}[]|\;:,<.>/?"\'"""), 'only one valid char'
    assert 'A' == comppart(r"""~!@#$%^&*()_=+{}[]|\;:,<.>/?"\'A"""), 'only one valid char'

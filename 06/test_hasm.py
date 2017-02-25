"""HASM unit tests."""

import imp
from collections import MutableMapping

import pytest


hasm = imp.load_source("hasm", "./hasm")  # noqa


@pytest.fixture
def patch_symbol_table(request, scope="function"):

    def _patcher(override):
        hasm._SYMBOL_TABLE.update(override)

    def _fin():
        hasm._SYMBOL_TABLE = hasm.create_builtins_symbol_table()

    request.addfinalizer(_fin)

    return _patcher


def test_create_builtins_symbol_table():

    assert isinstance(hasm.create_builtins_symbol_table(), MutableMapping)


def test_symbol_table():
    pass


def test_is_type():
    pass


@pytest.mark.parametrize(("symbol", "expected"), (
    (0, "0000000000000000"),
    (16, "0000000000010000"),
    ("17", "0000000000010001"),
    (65536, "10000000000000000"),
))
def test_to_word(symbol, expected):
    assert hasm.to_word(symbol) == expected


def test_to_word_negative():
    with pytest.raises(ValueError):
        hasm.to_word("test")


def test_ralloc():
    pass


def test_remove_inline_comment():
    pass


def test_parse_a_instruction():
    pass


def test_parse_c_instruction():
    pass


def test_process_label_declaration():
    pass


def test_expand_labels():
    pass


def test_assembler():
    pass


def test_parse_args():
    pass


def test_prepare_filenames():
    pass


def test_main():
    pass


@pytest.mark.parametrize(("functions", "data", "expected"), (
    ([], [], []),
    ([lambda x: x + 1], list(range(0, 5)), list(range(1, 6))),
    ([lambda x: x + 1, lambda x: x * 2], range(0, 5), range(2, 12, 2)),
))
def test_apply_functions(functions, data, expected):

    assert hasm.apply_functions(functions, data) == expected

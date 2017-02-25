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
    for addr in range(16, 20):
        assert hasm.ralloc() == addr


def test_ralloc_negative(patch_symbol_table):
    # We have only one free address
    patch_symbol_table({hasm.FREE_ADDRESS_SYMBOL: hasm.RAM_MAX_ADDRESS})
    assert hasm.ralloc() == hasm.RAM_MAX_ADDRESS
    # Now we run out of memory
    with pytest.raises(hasm.ExceededArchRAMLimit):
        hasm.ralloc()


@pytest.mark.parametrize(("instruction", "result"), (
    ("@LABELNAME  ", "@LABELNAME"),
    ("@LABELNAME // comm", "@LABELNAME"),
    ("    //    ", ""),
))
def test_remove_inline_comment(instruction, result):
    assert hasm.remove_inline_comment(instruction) == result


@pytest.mark.parametrize(("instruction", "machine_code", "override"), (
    ("@0", hasm.to_word(0), None),
    ("@15 // this is comment", hasm.to_word(15), None),
    ("@16", hasm.to_word(16), None),
    ("@variable", hasm.to_word(16), None),
    ("@LABELNAME", hasm.to_word(20), {"LABELNAME": hasm.to_word(20)}),
    ("@SCREEN", hasm.to_word(16384), None),
))
def test_parse_a_instruction(
        patch_symbol_table, instruction, machine_code, override
):
    if override:
        patch_symbol_table(override)
    assert hasm.parse_a_instuction(instruction) == machine_code


def test_parse_a_instruction_negative():
    with pytest.raises(hasm.UndeclaredLabel):
        hasm.parse_a_instuction("@UNDEFINED")


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


@pytest.mark.parametrize(("args", "result"), (
    (("test.asm",), ("test.asm", "test.hack")),
    (("test.asm", "newfile"), ("test.asm", "newfile")),
    (("test.asm", None, "kek"), ("test.asm", "test.kek")),
))
def test_prepare_filenames(args, result):
    assert hasm.prepare_filenames(*args) == result


def test_main():
    pass


@pytest.mark.parametrize(("functions", "data", "expected"), (
    ([], [], []),
    ([lambda x: x + 1], list(range(0, 5)), list(range(1, 6))),
    (
        [lambda x: x + 1, lambda x: x * 2],
        list(range(0, 5)), list(range(2, 12, 2))
    ),
))
def test_apply_functions(functions, data, expected):

    assert hasm.apply_functions(functions, data) == expected

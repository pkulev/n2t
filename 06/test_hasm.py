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


@pytest.mark.parametrize(("typ", "value"), (
    (hasm.COMMENT, "// this is comment"),
    (hasm.COMMENT, "    //this is comment"),
    (hasm.WHITESPACE, "   "),
    (hasm.WHITESPACE, ""),
    (hasm.WHITESPACE, "\t"),
    (hasm.INLINE_COMMENT, "@15 // comment"),
    (hasm.INLINE_COMMENT, "@15//comment"),
    (hasm.A_TYPE_INSTR, "@15"),
    (hasm.A_TYPE_INSTR, "@variable"),
    (hasm.A_TYPE_INSTR, "@LABEL"),
    (hasm.C_TYPE_INSTR, "0; JMP // jump"),
    (hasm.C_TYPE_INSTR, "0  ;   JMP // jump too"),
    (hasm.C_TYPE_INSTR, "AMD=M+1; JGE"),
    (hasm.LABEL_DECL, "(THIS_IS_LABEL) // lab1"),
    (hasm.LABEL_DECL, "(THIS IS LABEL TOO?) // lab2"),
    (hasm.LABEL_DECL, "()"),
))
def test_is_type(typ, value):
    assert hasm.is_type(typ, value)


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


@pytest.mark.parametrize(("instruction", "machine_code"), (
    ("0; JMP // ", "1110101010000111"),
    ("M = -1", "1110111010001000"),
    ("M =M+ 1//", "1111110111001000"),
    ("AMD   = D", "1110001100111000"),
))
def test_parse_c_instruction(instruction, machine_code):
    # Slighty redunant test, all cases are covered by functional tests
    assert hasm.parse_c_instruction(instruction) == machine_code


def test_process_label_declarations():
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

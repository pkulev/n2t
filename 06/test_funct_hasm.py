import imp
import logging
import os
import sys
import difflib

import pytest


hasm = imp.load_source("hasm", "./hasm")  # noqa

FIXTURES_DIR = "./fixtures/"
LOG = logging.getLogger(__name__)


@pytest.fixture
def clear_symbol_table():
	hasm._SYMBOL_TABLE = hasm.create_builtins_symbol_table()


@pytest.mark.parametrize("filename", ("simple", "rect", "pong"))
def test_hasm(tmpdir, clear_symbol_table, filename):

	hack_file = tmpdir.mkdir(filename).join(filename + ".hack").strpath
	orig_hack_file = os.path.join(FIXTURES_DIR, filename + ".hack")
	asm_file = os.path.join(FIXTURES_DIR, filename + ".asm")

	# patch args
	sys.argv = ["./hasm", "-o", hack_file, asm_file]

	hasm.main()
	with open(hack_file) as hack_f:
		translated_lines = hack_f.readlines()
	with open(orig_hack_file) as hack_f:
		original_lines = hack_f.readlines()

	differ = difflib.Differ()
	assert len(translated_lines) == len(original_lines)

	errored = False
	lineno = 0
	for line in differ.compare(translated_lines, original_lines):
		if line.startswith("  "):
			lineno += 1
		else:
			errored = True
			LOG.error("{0}: {1}".format(lineno, line))
	if errored:
		pytest.fail()

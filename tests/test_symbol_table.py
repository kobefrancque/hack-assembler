import pytest
import sys
import os

from src.symbol_table import SymbolTable

class TestSymbolTable:
    def test_predefined_symbols(self):
        table = SymbolTable()
        assert table.get_address('R0') == 0
        assert table.get_address('R15') == 15
        assert table.get_address('SCREEN') == 16384
        assert table.get_address('KBD') == 24576
    
    def test_add_entry(self):
        table = SymbolTable()
        table.add_entry('LOOP', 10)
        assert table.contains('LOOP')
        assert table.get_address('LOOP') == 10
    
    def test_contains(self):
        table = SymbolTable()
        assert table.contains('R0')
        assert not table.contains('RANDOM')
    
    def test_overwrite_symbol(self):
        table = SymbolTable()
        table.add_entry('TEST', 100)
        table.add_entry('TEST', 200)
        assert table.get_address('TEST') == 200
import unittest

from sexpdata import Symbol
from vimside import sexp

class TestSexp(unittest.TestCase):

    def test_basic_list(self):
        data = sexp.loads('(:hello "world" :foo "bar")')
        self.assertDictEqual(data, { "hello": "world", "foo": "bar"})

    def test_nested_dict(self):
        data = sexp.loads('(:return (:ok "hello") 3)')
        self.assertDictEqual(data[1], {"ok": "hello"})

    def test_does_not_dictify_empty_list(self):
        data = sexp.loads('()')
        self.assertListEqual(data, [])

    def test_does_not_dictify_odd_list(self):
        data = sexp.loads('(:return () 4)')
        self.assertListEqual(data, [Symbol(":return"), [], 4])

    def test_does_not_dictify_non_symbol_keys(self):
        data = sexp.loads('(:a "b" "c" "d")')
        self.assertListEqual(data, [Symbol(":a"), "b", "c", "d"])

    def test_does_not_dictify_non_column_keys(self):
        data = sexp.loads('(:a "b" c "d")')
        self.assertListEqual(data, [Symbol(":a"), "b", Symbol("c"), "d"])


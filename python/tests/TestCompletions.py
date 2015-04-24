import unittest
import vimside.env


class TestCompletions(unittest.TestCase):
    def setUp(self):
        self._env = vimside.env.VimsideEnv()
        self._completer = self._env.completions

    def test_format_type_sig_no_parens(self):
        sig = [[], "Unit"]
        self.assertEqual(self._completer._format_type_sig(sig), "Unit")

    def test_format_type_sig_no_params(self):
        sig = [[[]], "Unit"]
        self.assertEqual(self._completer._format_type_sig(sig), "(): Unit")

    def test_format_type_sig_normal_params(self):
        sig = [[[["x", "Int"]]], "Unit"]
        self.assertEqual(self._completer._format_type_sig(sig), "(x: Int): Unit")


import os
import unittest
import tests

class EnsimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hello = os.path.join(os.path.dirname(tests.__file__), "resources", "projects", "hello")

        cls._hello_dir = hello
        cls._hello_ensime = os.path.join(cls._hello_dir, ".ensime")

        if not os.path.exists(cls._hello_ensime):
            ret = os.system("cd %s && sbt gen-ensime" % hello)
            if ret:
                raise Exception("Unable to generate .ensime")

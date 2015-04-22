import unittest
import os
import vimside.command

class TestEnsimeStartStop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hello = os.path.join(os.path.dirname(__file__), "resources", "projects", "hello")

        cls._hello_dir = hello
        cls._hello_ensime = os.path.join(cls._hello_dir, ".ensime")

        if not os.path.exists(cls._hello_ensime):
            ret = os.system("cd %s && sbt gen-ensime" % hello)
            if ret:
                raise Exception("Unable to generate .ensime")

    def  test_find_ensime_conf(self):
        p = vimside.command._FindEnsimeConf(self._hello_dir)
        self.assertEquals(p, self._hello_ensime)

    def test_find_ensime_conf_in_parents(self):
        p = vimside.command._FindEnsimeConf(os.path.join(
            self._hello_dir, "src", "main", "scala"))
        self.assertEquals(p, self._hello_ensime)



        


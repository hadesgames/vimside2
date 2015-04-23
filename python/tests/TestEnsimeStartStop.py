import unittest
import os
import vimside.command
import vimside.env
import tempfile
import time

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


    def test_ensime_can_create_classpath(self):
        (_, filename) = tempfile.mkstemp()
        vimside.command._CreateClassPath(filename, "2.11.6", "0.9.10-SNAPSHOT")

        self.assertTrue(os.path.exists(filename))
        self.assertGreater(os.path.getsize(filename), 0)

    def test_ensime_start_stop(self):
        env = vimside.env.getEnv()
        env.cwd = self._hello_dir
        vimside.command.StartEnsime(env)

        ft = env.connection.responseFuture(vimside.rpc.connection_info())
        print(ft.result(5))

        vimside.command.StopEnsime(env)







        


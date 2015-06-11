import os

import vimside.ensime.conf

import tests.ensime

class TestConf(tests.ensime.EnsimeTestCase):
    def  test_find_ensime_conf(self):
        path = vimside.ensime.conf.locate_conf(self._hello_dir)
        self.assertEquals(path, self._hello_ensime)

    def test_find_ensime_conf_in_parents(self):
        path = vimside.ensime.conf.locate_conf(os.path.join(
            self._hello_dir, "src", "main", "scala"))
        self.assertEquals(path, self._hello_ensime)

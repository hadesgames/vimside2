import tests.ensime
from vimside.env import VimsideEnv

class TestEnv(tests.ensime.EnsimeTestCase):
    def test_initialization(self):
        env = VimsideEnv.from_path(self._hello_dir)


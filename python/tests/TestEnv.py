import tests.ensime
from vimside.env import VimsideEnv

import vimside.logger

LOGGER = vimside.logger.getLogger(__name__)


class TestEnv(tests.ensime.EnsimeTestCase):

    def test_initialization(self):
        LOGGER.debug("Loading env for %s" % self._hello_dir)

        VimsideEnv.from_path(self._hello_dir)

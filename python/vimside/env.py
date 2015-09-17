import vimside.logger
import vimside.notes
import vimside.rpc as rpc
from vimside.ensime.manager import EnsimeManager
from vimside.connection.ensime import EnsimeConnection

LOGGER = vimside.logger.getLogger(__name__)


class VimsideEnv(object):

    def __init__(self, manager):
        self._ensime = manager
        self._scala_notes = vimside.notes.Notes("scala")
        self._java_notes = vimside.notes.Notes("java")
        self._initialize_env()
        pass

    envs = {}

    @classmethod
    def from_path(cls, path):
        manager = EnsimeManager.from_path(path)
        path = manager.conf_path()

        if path not in cls.envs:
            cls.envs[path] = VimsideEnv(manager)

        return cls.envs[path]

    def _initialize_env(self):
        if not self._ensime.is_active():
            self._ensime.start().result(30)

        self._conn = EnsimeConnection(self._ensime.get_socket())

        self._setup_components()
        self._initialize_connection()

    def _initialize_connection(self):
        self._conn.response_ft(rpc.connection_info()).result(5)
        self._conn.response_ft(rpc.init_project(self._ensime.conf)).result(5)

    def _setup_components(self):
        self._scala_notes.setup(self._conn)
        self._java_notes.setup(self._conn)

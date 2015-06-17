#class VimsideEnv(object):
    #def __init__(self):
        #self.connection = None
        #self.conf = {}
        #self.ensime_process = None
        #self.completions = vimside.completions.Completer(self)
        #self.typeinfo = vimside.typeinfo.TypeInfo(self)
        #self.refactor = vimside.refactor.Refactor(self)

    #def handle_connection_info(self, resp):
        #msg = resp.result()
        #msg = msg['ok']

        #print("Initialized %s %s" % (msg["implementation"]["name"], msg["version"]))

    #def initialize_connection(self, connection):
        #self.connection = connection

        #self.connection.responseFuture(rpc.connection_info()).add_done_callback(
                #self.handle_connection_info)
        #self.connection.responseFuture(rpc.init_project(self.conf))


    #def is_ready(self):
        #return self.connection is not None
import vimside.logger
import vimside.rpc as rpc
from vimside.ensime.manager import EnsimeManager
from vimside.connection.ensime import EnsimeConnection

LOGGER = vimside.logger.getLogger(__name__)

class VimsideEnv(object):
    def __init__(self, manager):
        self._ensime = manager
        self._initialize_env()
        pass

    envs = {}
    @classmethod
    def from_path(cls, path):
        manager = EnsimeManager.from_path(path)
        path = manager.conf_path()

        if not path in cls.envs:
            cls.envs[path] = VimsideEnv(manager)

        return cls.envs[path]

    def _initialize_env(self):
        if not self._ensime.is_active():
            self._ensime.start().result(5)

        self._conn = EnsimeConnection(self._ensime.get_socket())

        self._initialize_connection()

    def _initialize_connection(self):
        self._conn.response_ft(rpc.connection_info()).result(5)
        self._conn.send(rpc.init_project(self._ensime.conf))

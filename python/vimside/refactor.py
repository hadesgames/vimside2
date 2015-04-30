import threading
import vimside.rpc as rpc

class Refactor(object):
    def __init__(self, env):
        self._env = env
        self._refactor_id = 0
        self._refactor_id_lock = threading.Lock()

    def _get_id(self):
        with self._refactor_id_lock:
            self._refactor_id += 1
            return self._refactor_id

    def execute_add_import(self, filename, name):
        _id = self._get_id()

        req = rpc.prepare_refactor(_id, "addImport", {
            'qualifiedName': name,
            'file': filename}, True)

        self._env.connection.responseFuture(req).result()

        return 0


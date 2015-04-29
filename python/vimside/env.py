import vimside 
import vimside.completions
import vimside.typeinfo

from vimside import rpc
class VimsideEnv(object):
    def __init__(self):
        self.connection = None
        self.conf = {}
        self.ensime_process = None
        self.completions = vimside.completions.Completer(self)
        self.typeinfo = vimside.typeinfo.TypeInfo(self)

    def handle_connection_info(self, resp):
        msg = resp.result()
        msg = msg['ok']

        print("Initialized %s %s" % (msg["implementation"]["name"], msg["version"]))

    def initialize_connection(self, connection):
        self.connection = connection

        self.connection.responseFuture(rpc.connection_info()).add_done_callback(
                self.handle_connection_info)
        self.connection.responseFuture(rpc.init_project(self.conf))


    def is_ready(self):
        return self.connection is not None

global_env = VimsideEnv()

def getEnv():
    return global_env



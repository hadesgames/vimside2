import vim
from vimside import rpc
class VimsideEnv(object):
    def __init__(self):
        self.connection = None
        self.conf = {}
        self.ensime_process = None

    def handle_connection_info(self, msg):
        msg = msg['ok']

        print("Initialized %s %s" % (msg["implementation"]["name"], msg["version"]))

    def set_connection(self, conn):
        self.connection = conn

        self.connection.send(rpc.connection_info(), self.handle_connection_info)

global_env = VimsideEnv()

def getEnv():
    return global_env



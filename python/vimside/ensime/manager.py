import vimside.logger
from vimside.ensime.conf import locate_conf_dir, load_conf_from_dir, conf_from_dir
from vimside.ensime.command import start_command

import os
import socket
import subprocess

LOGGER = vimside.logger.getLogger(__name__)

class EnsimeManager(object):
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.ensime_process = None
        self.reload_conf()

    @classmethod
    def from_path(cls, path):
        return EnsimeManager(locate_conf_dir(path))


    def reload_conf(self):
        self.conf = load_conf_from_dir(self.base_dir)

    def conf_path(self):
        return conf_from_dir(self.base_dir)
    def port_path(self):
        return os.path.join(self.conf['cache-dir'], 'port')

    def port(self):
        port = 0
        with open(self.port_path(), "r") as fh:
            port = int(fh.read())

        return port

    def is_active(self):
        return os.path.exists(self.port_path())

    def get_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", self.port()))

        return sock

    def start(self):
        cmd = start_command(self.conf_path())
        with open("/tmp/ENSIME_LOG", "a") as fh:
            self.ensime_process = subprocess.Popen(cmd, stdout=fh, stderr=fh)

    def stop(self):
        # TODO wait for terminate else kill
        if self.ensime_process is not None:
            self.ensime_process.terminate()

        self.ensime_process = None

import os
import vimside.logger
import vimside.sexp

LOGGER = vimside.logger.getLogger(__name__)

class NoEnsimeConf(Exception):
    pass

def locate_conf(_dir):
    file_name = ".ensime"
    while _dir != "/":
        conf = os.path.join(_dir, file_name)
        LOGGER.debug("Checking %s", conf)

        if os.path.exists(conf):
            return conf

        _dir = os.path.dirname(_dir)

    raise NoEnsimeConf

def load_conf(filename):
    with open(filename, "r") as conf:
        return vimside.sexp.load(conf)

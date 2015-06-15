import os
import vimside.logger
import vimside.sexp

LOGGER = vimside.logger.getLogger(__name__)

class NoEnsimeConf(Exception):
    pass

def locate_conf_dir(_dir):
    filename = ".ensime"
    while _dir != "/":
        conf = os.path.join(_dir, filename)
        LOGGER.debug("Checking %s", conf)

        if os.path.exists(conf):
            return _dir

        _dir = os.path.dirname(_dir)

    raise NoEnsimeConf

def conf_from_dir(_dir):
    return os.path.join(_dir, ".ensime")

def load_conf_from_dir(_dir):
    filename = conf_from_dir(_dir)
    with open(filename, "r") as conf:
        return vimside.sexp.load(conf)

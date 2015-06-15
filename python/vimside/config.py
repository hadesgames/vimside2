import vimside

import ConfigParser
import os

def load_cfg():
    default = os.path.join(
        vimside.root(), 'resources', 'cfg', 'defaults.cfg')

    config = ConfigParser.ConfigParser()
    config.readfp(open(default))

    return config

config = load_cfg()


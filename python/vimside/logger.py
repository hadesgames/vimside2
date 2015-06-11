import logging

_logger = None


def getRootLogger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger("vimside2")
    return _logger

def getLogger(name):
    return getRootLogger().getChild(name)

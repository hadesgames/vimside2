from sexpdata import Symbol

def connection_info():
    return [Symbol("swank:connection-info")]

def shutdown_server():
    return [Symbol("swank:shutdown-server")]

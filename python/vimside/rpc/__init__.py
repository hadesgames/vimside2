from sexpdata import Symbol

def connection_info():
    return [Symbol("swank:connection-info")]

def shutdown_server():
    return [Symbol("swank:shutdown-server")]

def completions(filename, offset, max_results=0, match_case=True, reload_file = True):
    return [
            Symbol("swank:completions"),
            { "file": filename },
            offset,
            max_results,
            match_case,
            reload_file]

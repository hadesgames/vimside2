from sexpdata import Symbol

def connection_info():
    return [Symbol("swank:connection-info")]

def shutdown_server():
    return [Symbol("swank:shutdown-server")]

def init_project(conf):
    return [Symbol("swank:init-project"), conf]

def completions(filename, offset, max_results=0, match_case=True, reload_file = True):
    return [
            Symbol("swank:completions"),
            { "file": filename },
            offset,
            max_results,
            match_case,
            reload_file]

def type_at_point(filename, start, end = None):
    if end is None:
        point = start
    else:
        point = [start, end]


    return [
            Symbol("swank:type-at-point"),
            filename,
            point 
           ]

def symbol_at_point(filename, offset):
    return [
            Symbol("swank:symbol-at-point"),
            filename,
            offset 
           ]

def typecheck_file(filename):
    return [
            Symbol("swank:typecheck-file"),
            { "file": filename }
           ]

def import_suggestions(filename, offset):
    return [
            Symbol("swank:import-suggestions"),
            filename,
            offset,
            ["Future"],
            10
           ]

def prepare_refactor(_id, tpe, data, now):
    return [
            Symbol("swank:prepare-refactor"),
            _id,
            Symbol(tpe),
            [Symbol("file"), data['file'], Symbol('qualifiedName'), data['qualifiedName']],
            False
           ]

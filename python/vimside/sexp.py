import sexpdata

def _dictify(sexp):
    if not type(sexp) == list:
        return sexp

    sexp = [ _dictify(elem) for elem in sexp ]

    if len(sexp) % 2 != 0:
        return sexp

    if len(sexp) == 0:
        return sexp

    symbol_keys = True
    for key in sexp[::2]:
        if type(key) != sexpdata.Symbol or not key.value().startswith(":"):
            symbol_keys = False
            break
    if not symbol_keys:
        return sexp

    d = { k.value()[1:] : v for k, v in zip(sexp[::2], sexp[1::2]) }

    return d

def loads(s, **kwargs):
    data = sexpdata.loads(s, **kwargs)

    return _dictify(data)



def dumps(obj, **kwargs):
    return sexpdata.dumps(obj, **kwargs)


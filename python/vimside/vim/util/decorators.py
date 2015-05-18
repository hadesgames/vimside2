import vim

def filename(f):
    def newf(*args, **kwargs):
        filename = vim.eval('expand("%:p")')
        return f(*args, filename=filename, **kwargs)

    return newf

def offset(f):
    def newf(*args, **kwargs):
        offset = int(vim.eval('line2byte(line("."))+col(".")-2'))
        return f(*args, offset=offset, **kwargs)

    return newf


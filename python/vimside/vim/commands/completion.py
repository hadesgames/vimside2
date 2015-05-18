import vim

from vimside.vim.util.decorators import filename, offset

_completions = None

@filename
@offset
def OmniComplete(env, find_start, base, filename, offset):
    global _completions

    if find_start:
        vim.command("w!")
        _completions = env.completions.get_completions(filename, offset).result(5)

        return int(vim.eval('col(".")')) - len(_completions["prefix"]) - 1
    else:
        result = _completions["completions"]
        _completions = None

        return result

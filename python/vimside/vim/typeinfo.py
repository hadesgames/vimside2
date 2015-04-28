import re
import vim
import vimside.env
import vimside.rpc as rpc
import logging

def _is_operator_part(c):
    return re.match(r"[~!@%^*+-<>?:=&|/\\]", c)

def _find_word_at(col):
    logging.info("Searching for scala word at %s", col)
    def find(p):
        if col >= len(vim.current.line):
            return (col, col)
        start = col
        while start >= 0 and p(vim.current.line[start]):
            start -= 1
        start += 1

        end = col
        while end < len(vim.current.line) and p(vim.current.line[end]):
            end += 1

        end -= 1

        return (start, end)

    (start, end) = find(lambda c: re.match(r"[\w_]", c))

    logging.info("Found word in range (%s, %s) => '%s'", start, end, vim.current.line[start: end + 1])

    if start > col or end < col:
        return find(lambda c: _is_operator_part(c))
    else:
        return (start, end)

def showStatus(status):
    print(status)

def showTypeAt(env, filename, col):
    if not env.is_ready():
        return 0

    def handleSymbolInfo(resp):
        tpe = env.typeinfo.format_symbol(resp.result()["ok"])
        if tpe is not None:
            showStatus(tpe)

    def handleTypeInfo(resp):
        tpe = env.typeinfo.format_type_info(resp.result()["ok"])
        if tpe is None:
            env.typeinfo.askSymbolInfo(filename, current).add_done_callback(handleSymbolInfo)
        else:
            showStatus(tpe)

    word = _find_word_at(col)
    line_offset = int(vim.eval("line2byte(line('.'))"))
    start = word[0] + line_offset
    end = word[1] + line_offset
    current = line_offset + col

    env.typeinfo.askTypeInfo(filename, start, end).add_done_callback(handleTypeInfo)

    return 0



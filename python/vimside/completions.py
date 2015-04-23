import vimside.rpc as rpc
class Completer(object):
    def __init__(self, env):
        self._env = env


    def get_completions(self, filename, offset):
        req = rpc.completions(filename, offset)

        res = self._env.connection.responseFuture(req).result(5)["ok"]
        res["completions"] = self._to_vim_format(res["completions"])

        return res

    def _to_vim_format(self, completions):
        return {
                'words': [self._format_completion(comp) for comp in completions],
                'refresh': 'always'}

    def _format_completion(self, completion):
        return {
                'word': completion["name"],
                'menu': str(completion["type-sig"]),
                'kind': 'f' if completion["is-callable"] else "m"
                }




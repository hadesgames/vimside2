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


    def _format_call(self, call):
        params = self._format_params(call)

        return "(%s)" % params

    def _format_calls(self, calls):
        return "".join([self._format_call(call) for call in calls])

    def _format_type_sig(self, sig):
        # We expect type sig to a be a tuple with the list of calls and the return type
        calls = self._format_calls(sig[0])
        if len(sig[0]) == 0:
            return "%s" % sig[1]
        else:
            return "%s: %s" % (calls, sig[1])


    def _format_param(self, param):
        return "%s: %s" % (param[0], param[1])

    def _format_params(self, params):
        return ", ".join([self._format_param(param) for param in params])

    def _format_completion(self, completion):
        return {
                'word': completion["name"],
                'menu': self._format_type_sig(completion["type-sig"]),
                'kind': 'f' if completion["is-callable"] else "m"
                }

    def get_import_suggestions(self, filename, offset):
        msg = self._env.connection.responseFuture(rpc.import_suggestions(filename, offset)).result()["ok"]
        if type(msg) != list:
            return []

        if len(msg) == 0:
            return []

        return [imp['name'] for imp in msg[0]]






import vimside.rpc as rpc

import logging

class cached(object):
    def __init__(self, f):
        self._f = f
        self._last_request = None
        self._pending_response = None

    def __get__(self, instance, owner):
      self.obj = instance

      return self.__call__

    def __call__(self, *args):
        resp = self._pending_response

        if self._last_request== args:
            logging.debug("Cache hit on %s", args)
            return resp
        
        if resp is not None:
            resp.cancel()
        
        self._last_request = args

        resp = self._f(self.obj, *args)
        self._pending_response = resp

        return resp

class TypeInfo(object):
    def __init__(self, env):
        self._env = env
        self._last_request = None
        self._pending_response = None

    def askTypeInfo(self, filename, start, end = None):
        if end is None:
            end = start
        return self._env.connection.responseFuture(rpc.type_at_point(filename, start, end))

    @cached
    def askCachedTypeInfo(self, *args):
        return self.askTypeInfo(*args)

    def askSymbolInfo(self, filename, offset):
        return self._env.connection.responseFuture(rpc.symbol_at_point(filename, offset))

    @cached
    def askCachedSymbolInfo(self, *args):
        return self.askSymbolInfo(*args)


    def format_type_info(self, tpe):
        if type(tpe) != dict:
            return None

        if tpe.get("name", None) == "<notype>":
            return None

        if "full-name" in tpe:
            return tpe["full-name"]

        return tpe.get("name", None)

    def format_symbol(self, symbol):
        if type(symbol) != dict:
            return None

        if not "type" in symbol:
            return None

        return self.format_type_info(symbol["type"])




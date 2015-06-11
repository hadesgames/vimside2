# pylint: disable=missing-docstring
import sexpdata
import concurrent
import vimside.logger
from vimside.connection.base import BaseSwankConnection

LOGGER = vimside.logger.getLogger("connection.swank")

class ResponseHandler(object):
    def __init__(self, conn):
        super(ResponseHandler, self).__init__()
        self._conn = conn

    def can_handle(self, msg):
        if not isinstance(msg, list) or len(msg) == 0:
            LOGGER.debug("Response Handler - check 1 - ignoring  message: %s", msg)
            return False

        if not isinstance(msg[0], sexpdata.Symbol) or msg[0].value() != ":return":
            LOGGER.debug("Response Handler 2 - check 2 - ignoring message: %s", msg)
            return False

        if not self._conn.awaiting_response(msg[2]):
            return False

        return True

    def handle(self, msg):
        LOGGER.info("ResponseHandler - got %s", msg)
        self._conn.complete_response(msg[1], msg[2])

class SwankConnection(BaseSwankConnection):
    def __init__(self, *args, **kwargs):
        super(SwankConnection, self).__init__(*args, **kwargs)
        self._response_promises = {}
        self._response_handler = ResponseHandler(self)

        self.received.filter(self.is_response) \
                     .subscribe(self._response_handler.handle)

    def response_ft(self, req):
        _id = self.get_id()
        future = concurrent.futures.Future()
        self._response_promises[_id] = future

        self.send(req, _id)

        return future

    def is_response(self, msg):
        return self._response_handler.can_handle(msg)

    def awaiting_response(self, _id):
        return _id in self._response_promises

    def complete_response(self, resp, _id):
        future = self._response_promises[_id]

        if future.set_running_or_notify_cancel():
            future.set_result(resp)

        del self._response_promises[_id]

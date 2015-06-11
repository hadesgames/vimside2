import sexpdata
import concurrent
import vimside.logger
from vimside.connection.base import BaseSwankConnection

logger = vimside.logger.getLogger("connection.swank")

class ResponseHandler(object):
    def __init__(self, conn):
        super(ResponseHandler, self).__init__()
        self._conn = conn

    def can_handle(self, msg):
        if not type(msg) == list or len(msg) == 0:
            logger.debug("Response Handler - check 1 - ignoring  message: %s", msg)
            return False

        if type(msg[0]) != sexpdata.Symbol or msg[0].value() != ":return":
            logger.debug("Response Handler 2 - check 2 - ignoring message: %s", msg)
            return False

        if self._conn.awaitingResponse(msg[2]):
            return False

        return True

    def handle(self, msg):
        logger.info("ResponseHandler - got %s", msg)
        self._conn.completeResponse(msg[1], msg[2])

class SwankConnection(BaseSwankConnection):
    def __init__(self, *args, **kwargs):
        super(SwankConnection, self).__init__(*args, **kwargs)
        self._response_promises = {}
        self._response_handler = ResponseHandler(self)

        self.received.filter(self.isResponse) \
                     .subscribe(self._response_handler.handle)

    def responseFuture(self, req):
        _id = self.get_id()
        ft = concurrent.futures.Future()
        self._response_promises[_id] = ft

        self.send(req, _id)

        return ft

    def isResponse(self, msg):
        return self._response_handler.can_handle(msg)

    def awaitingResponse(self, _id):
        _id in self._response_promises

    def completeResponse(self, resp, _id):
        ft = self._response_promises[_id]

        if ft.set_running_or_notify_cancel():
            ft.set_result(resp)

        del self._response_promises[_id]

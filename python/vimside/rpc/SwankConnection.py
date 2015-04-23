import socket
import Queue
import threading

import sexpdata
import vimside.sexp
import logging
import concurrent.futures

logging.basicConfig(filename='/tmp/VIMSIDE_LOG', level=logging.DEBUG)

logger = logging.getLogger("swank-connection")

class BaseSwankConnection(object):
    def __init__(self, socket, spawn_read_thread=True, spawn_write_thread=True):
        self._socket = socket
        self._outgoing = Queue.Queue()
        self._id = 0
        self._id_lock = threading.Lock()

        if spawn_read_thread:
            self._read_thread = threading.Thread(name="swank-read-thread", target=self._receive_loop)
            self._read_thread.setDaemon(True)
            self._read_thread.start()

        if spawn_write_thread:
            self._write_thread = threading.Thread(name="swank-write-thread", target=self._send_loop)
            self._write_thread.setDaemon(True)
            self._write_thread.start()

    def __del__(self):
        self._socket.close()

    def get_id(self):
        with self._id_lock:
            self._id +=1
            return self._id

    def send(self, req, _id = None):
        if _id is None:
            _id = self.get_id()

        self._outgoing.put((req, _id))

        return _id

    def _send_loop(self):
        while True:
            self._send_next_msg()

    def _send_next_msg(self):
       (req, _id) = self._outgoing.get()

       self._socket.send(self._prepare_req(req, _id))
       self._outgoing.task_done()


    def _encode_length(self, msg):
        l = hex(len(msg))[2:]

        return '0' * (6 - len(l)) + l


    def _prepare_req(self, payload, _id):
        req = vimside.sexp.dumps([sexpdata.Symbol(':swank-rpc'), payload, _id])

        req = req.encode("UTF-8")
        length = self._encode_length(req)

        return length + req


    def _receive_loop(self):
        while True:
            self._receive_incomming_msg()

    def _receive_incomming_msg(self):
        length = int(self._socket.recv(6), 16)
        resp_str = self._socket.recv(length)

        logger.debug("Received message %s", resp_str)

        resp = vimside.sexp.loads(resp_str)

        self._handle_incomming_msg(resp)


    def _handle_incomming_msg(self, msg):
        raise NotImplementedError



class SwankConnection(BaseSwankConnection): 

    def __init__(self, *args, **kwargs):
        super(SwankConnection, self).__init__(*args, **kwargs)
        self._response_handlers = {}
        self._handlers = [
                ResponseHandler(self._response_handlers),
                EventHandler()]

    def responseFuture(self, req):
        ft = concurrent.futures.Future()

        def _handle(msg):
            if ft.set_running_or_notify_cancel():
                ft.set_result(msg)

        self.send(req, _handle)
        return ft


    def send(self, req, handler):
        _id = self.get_id()
        self._response_handlers[_id] = handler

        super(SwankConnection, self).send(req, _id)


    def _handle_incomming_msg(self, msg):
        dispatched = False
        for handler in self._handlers:
            if handler.can_handle(msg):
                dispatched = True
                handler.handle(msg)

        if not dispatched:
            logger.warning("No handlers found. Dropping message %s", msg)

class Handler(object):
    def can_handle(self, msg):
        raise NotImplementedError
    def handle(self, msg):
        raise NotImplementedError

class EventHandler(Handler):
    def can_handle(self, msg):
        return type(msg) == dict

    def handle(self, msg):
        logger.warning("Doing nothing on event %s", msg)

class ResponseHandler(Handler):
    def __init__(self, handlers):
        super(ResponseHandler, self).__init__()
        self._handlers = handlers

    def can_handle(self, msg):
        if not type(msg) == list or len(msg) == 0:
            logger.debug("Response Handler - check 1- ignoring  message: %s", msg)
            return False

        if type(msg[0]) != sexpdata.Symbol or msg[0].value() != ":return":
            logger.debug("Response Handler 2 - check 2 - ignoring message: %s", msg)
            return False

        if msg[2] not in self._handlers:
            return False

        return True

    def handle(self, msg):
        logger.info("ResponseHandler - got %s", msg)
        self._handlers[msg[2]](msg[1])
        del self._handlers[msg[2]]


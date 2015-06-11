# pylint: disable=missing-docstring
import Queue
import rx.subjects
import threading
import vimside.logger
import vimside.sexp
import sexpdata

LOGGER = vimside.logger.getLogger("connection.base")

class BaseSwankConnection(object):
    def __init__(self, socket, spawn_read_thread=True, spawn_write_thread=True):
        self._socket = socket
        self._outgoing = Queue.Queue()
        self._id = 0
        self._id_lock = threading.Lock()
        self._received_subject = rx.subjects.Subject()

        if spawn_read_thread:
            self._read_thread = threading.Thread(
                name="swank-read-thread",
                target=self._receive_loop)
            self._read_thread.setDaemon(True)
            self._read_thread.start()

        if spawn_write_thread:
            self._write_thread = threading.Thread(
                name="swank-write-thread",
                target=self._send_loop)
            self._write_thread.setDaemon(True)
            self._write_thread.start()

    def __del__(self):
        self._socket.close()

    @property
    def received(self):
        return self._received_subject

    def send(self, req, _id=None):
        if _id is None:
            _id = self.get_id()

        self._outgoing.put((req, _id))

        return _id

    def get_id(self):
        with self._id_lock:
            self._id += 1
            return self._id


    def _send_loop(self):
        while True:
            self._send_next_msg()

    def _send_next_msg(self):
        (req, _id) = self._outgoing.get()

        self._socket.send(self._prepare_req(req, _id))
        self._outgoing.task_done()

    @classmethod
    def encode_length(cls, msg):
        length = hex(len(msg))[2:]

        return '0' * (6 - len(length)) + length


    def _prepare_req(self, payload, _id):
        req = vimside.sexp.dumps([sexpdata.Symbol(':swank-rpc'), payload, _id])

        req = req.encode("UTF-8")
        length = self.encode_length(req)

        return length + req


    def _receive_loop(self):
        while True:
            self._receive_incomming_msg()

    def _receive_incomming_msg(self):
        length = int(self._socket.recv(6), 16)

        resp_str = ""
        while length > 0:
            chunk = self._socket.recv(length)
            resp_str += chunk
            length -= len(chunk)

        LOGGER.debug("Received message %s", resp_str)

        resp = vimside.sexp.loads(resp_str)

        self._handle_incomming_msg(resp)


    def _handle_incomming_msg(self, msg):
        self._received_subject.on_next(msg)



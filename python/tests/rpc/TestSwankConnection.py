import unittest
from mock import MagicMock
from vimside.rpc.SwankConnection import SwankConnection
import Queue
import sexpdata
from time import sleep

class MockSocket:
    def __init__(self, data):
        self._data = data
        self.received = ""

    def recv(self, size):
        res = self._data[:size]
        self._data = self._data[size:]
        return res

    def send(self, data):
        self.received += data

    def close(self):
        pass

class TestSwankConnection(unittest.TestCase):
    def setUp(self):
        self._socket = MockSocket("000002()")
        self._conn = SwankConnection(self._socket, spawn_read_thread=False, spawn_write_thread=False)

    def tearDown(self):
        del self._conn

    def test_send_request(self):
        req = [sexpdata.Symbol("swank:connection-info")]
        self._conn.send(req, lambda x: x)
        self._conn._send_next_msg()

        self.assertEqual(self._socket.received, "000026(:swank-rpc (swank:connection-info) 1)")

    def test_read_request_should_handle_missing_handlers(self):
        self._socket._data = '000054(return (:ok (:pid nil :server-implementation (:name "ENSIME") :version "0.0.1")) 1)'
        self._conn._receive_incomming_msg()

    def test_handlers(self):
        # Send Request
        req = [sexpdata.Symbol("swank:connection-info")]
        ft = self._conn.responseFuture(req)
        self._conn._send_next_msg()

        # Send Response
        self._socket._data = '000055(:return (:ok (:pid nil :server-implementation (:name "ENSIME") :version "0.0.1")) 1)'
        self._conn._receive_incomming_msg()

        resp = ft.result(1)
        self.assertEquals(type(resp), dict)
        self.assertTrue("ok" in resp)
        self.assertEquals(resp["ok"]["version"], "0.0.1")




    def test_handles_events(self):
        self._socket._data = '000011(:compiler-ready)'
        self._conn._receive_incomming_msg()



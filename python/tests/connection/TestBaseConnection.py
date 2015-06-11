import unittest
from vimside.connection.base import BaseSwankConnection
import sexpdata

class MockSocket(object):
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

class TestBaseConnection(unittest.TestCase):
    def setUp(self):
        self._socket = MockSocket("000002()")
        self._conn = BaseSwankConnection(
            self._socket,
            spawn_read_thread=False,
            spawn_write_thread=False)

    def tearDown(self):
        del self._conn

    def test_send_request(self):
        req = [sexpdata.Symbol("swank:connection-info")]
        self._conn.send(req)
        self._conn._send_next_msg()

        self.assertEqual(self._socket.received, "000026(:swank-rpc (swank:connection-info) 1)")

    def test_receive_request(self):
        received = self._conn.received.to_list().to_future()

        self._socket._data = '000054(return (:ok (:pid nil :server-implementation (:name "ENSIME") :version "0.0.1")) 1)'
        self._conn._receive_incomming_msg()
        self._conn.received.on_completed()

        res = received.result()

        self.assertEqual(len(res), 1)

        msg = res[0]
        self.assertEqual(len(msg), 3)
        self.assertEqual(msg[0], sexpdata.Symbol('return'))
        self.assertEqual(msg[2], 1)

        self.assertDictEqual(msg[1], {
            'ok': {
                'pid': [],
                'server-implementation': {'name': 'ENSIME'},
                'version': '0.0.1',
            }
        })


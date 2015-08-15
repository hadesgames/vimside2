#pylint: disable=missing-docstring
import sexpdata
import vimside.logger
from vimside.connection.swank import SwankConnection

LOGGER = vimside.logger.getLogger("connection.ensime")

class EnsimeConnection(SwankConnection):
    def __init__(self, *args, **kwargs):
        super(EnsimeConnection, self).__init__(*args, **kwargs)
        self._events = self.received.filter(
            lambda msg: not self.is_response(msg))


    @property
    def all_events(self):
        return self._events


    def events(self, name):
        return self._events.filter(
            lambda event: self.is_event_with_name(event, name))


    @classmethod
    def is_event_with_name(cls, event, name):
        if not isinstance(event, list) or len(event) == 0:
            return False

        if  isinstance(event[0], sexpdata.Symbol):
            return False

        if event[0].value() != name:
            return False
        return True

import concurrent
import vimside.logger
from vimside.connection.swank import SwankConnection

logger = vimside.logger.getLogger("connection.ensime")

class EnsimeConnection(SwankConnection):
    def __init__(self, *args, **kwargs):
        super(EnsimeConnection, self).__init__(*args, **kwargs)
        self._events = self.received.filter(
                lambda msg: not self.isResponse(msg))


    @property
    def all_events(self):
        return self._events


    def events(self, name):
        return self.events.filter(
                lambda event: self.isEventWithName(event, name))


    def is_event_with_name(self, event, name):
        if not type(event) != list or len(event) == 0:
            return False

        if  type(msg[0]) != sexpdata.Symbol:
            return False

        if msg[0].value() != name:
            return False
        return True




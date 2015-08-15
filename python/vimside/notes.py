
class Notes(object):
    def __init__(self, tpe):
        self._type = tpe
        self._notes = []

    def setup(self, conn):
        conn.events("clear-all-%s-notes" % self._type).subscribe(self.clear)
        conn.events("%s-notes" % self._type).subscribe(self.notes)
    
    def clear(self, _):
        self._notes = []

    def notes(self, ev):
        pass



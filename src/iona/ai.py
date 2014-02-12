import json
import logging
import time

logger = logging.getLogger(__name__)


class Iona:

    ATTRS = ('emotions',)
    EMOTIONS = ('happy',)

    def dump(self, file):
        """Dump the instance to the given file object"""
        data = dict()
        for attr in self.ATTRS:
            try:
                data[attr] = getattr(self, attr)
            except AttributeError:
                logger.warning("Undefined attribute while dumping: {}".format(
                    attr))
                data[attr] = None
        json.dump(data, file)

    @classmethod
    def load(self, in_buffer, out_buffer, file):
        """Load an instance from the given file object"""
        data = json.load(file)
        return self(in_buffer, out_buffer, data)

    def __init__(self, in_buffer, out_buffer, data=None):
        """Init an instance of Iona using a data dict.

        Init a fresh instance of Iona if data is None or not given.

        """
        self.in_buffer = in_buffer
        self.out_buffer = out_buffer
        if data is not None:
            for key in data:
                setattr(self, key, data[key])
        else:
            self._new()

    def _new(self):
        self.emotions = dict((x, 0) for x in self.EMOTIONS)

    def start(self):
        start = time.perf_counter()
        while True:
            time.sleep(1/60)
            end = time.perf_counter()
            self.run(start - end)
            start = end

    def run(self, dt):
        if self.in_buffer:
            mesg = self.in_buffer.read()
            if mesg:
                self.out_buffer.write(mesg)

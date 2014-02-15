import json
import logging
import time

from iona import emotion

logger = logging.getLogger(__name__)


class Iona:

    ATTRS = (
        ('emotions', (
            ('happiness', emotion.Happiness),
        )),
    )

    def dump(self, file):
        """Dump the instance to the given file object"""
        data = dict()
        for attr, _ in self.ATTRS:
            try:
                data[attr] = getattr(self, attr)
            except AttributeError:
                logger.warning("Undefined attribute while dumping: {}".format(
                    attr))
                data[attr] = None
        self._translate_dump(data)
        json.dump(data, file)

    @classmethod
    def _translate_dump(cls, data):
        "Translate an attribute dict to JSON compatible format in place"""
        for attr, keys in cls.ATTRS:
            values = data[attr]
            for key, _ in keys:
                try:
                    x = values[key].dump()
                except AttributeError:
                    logger.warning("Failed to call dump() on {}".format(
                        values[key]))
                else:
                    values[key] = x

    @classmethod
    def load(self, in_buffer, out_buffer, file):
        """Load an instance from the given file object"""
        data = json.load(file)
        return self(in_buffer, out_buffer, data)

    @classmethod
    def _translate_load(cls, data):
        "Translate an attribute dict from JSON compatible format in place"""
        for attr, keys in cls.ATTRS:
            values = data[attr]
            for key, constructor in keys:
                values[key] = constructor(values[key])

    def __init__(self, in_buffer, out_buffer, data=None):
        """Init an instance of Iona using a data dict.

        Init a fresh instance of Iona if data is None or not given.

        """
        self.in_buffer = in_buffer
        self.out_buffer = out_buffer
        if data is not None:
            self._translate_load(data)
            for key in data:
                setattr(self, key, data[key])
        else:
            self._new()

    def _new(self):
        for attr, keys in self.ATTRS:
            setattr(self, attr, dict(
                (key, constructor(0)) for key, constructor in keys))

    def start(self):
        start = time.perf_counter()
        while True:
            time.sleep(1/60)
            end = time.perf_counter()
            self.run(start - end)
            start = end

    def run(self, dt):
        if self.in_buffer:
            mesg = self.in_buffer.read().decode()
            if mesg is not None:
                self.out_buffer.write(','.join((
                    mesg,
                    "Happiness: {}".format(self.emotions['happiness'].value)
                )).encode())

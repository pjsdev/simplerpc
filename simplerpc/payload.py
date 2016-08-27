import json

from exceptions import MalformedPayload
from config import Config

class Payload:
    """
    Namespace for payload encoding/decoding
    """

    class BufferDecoder:
        def __init__(self):
            self.dangling = ''

        def packages(self, buf):
            while True:
                eof = buf.find('\n')
                if eof is -1: # didnt find end of message
                    self.dangling += buf
                    break

                pkg = self.dangling + buf[:eof]
                buf = buf[eof+1:]
                self.dangling = ''

                yield pkg

    @staticmethod
    def from_string(data):
        """
        Return tuple:
            (int opcode, dict data) -> the rpc

        Raise:
            MalformedPayload -> simple rpc fail
        """
        try:
            json_start = data.index("{")
        except ValueError:
            raise MalformedPayload("JSON data not found")

        opcode = data[:json_start]

        if opcode == "":
            raise MalformedPayload("Could not find opcode")

        json_string = data[json_start:]
        json_string = json_string.strip()

        try:
            args = json.loads(json_string)
        except ValueError:
            raise MalformedPayload("JSON malformed for opcode: %s" % opcode)

        return (opcode, args)

    @staticmethod
    def to_string(opcode, args):
        """
        Return string representing a simplerpc message

        Raises:
            ValueError if we cannot convert opcode to string or
            parse JSON
        """
        # Note: no net_id is ever input into message
        return "{}{}\n".format(opcode, json.dumps(args))

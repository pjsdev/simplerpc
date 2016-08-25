import json

from exceptions import MalformedPayload
from util import Util

class Payload:
    @staticmethod
    def from_string(data):
        try:
            json_start = data.index("{")
        except ValueError:
            raise MalformedPayload("JSON data not found")

        opcode = int(data[:json_start])

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
        # Note: no net_id is ever input into message
        payload = "{}{}".format(str(opcode), json.dumps(args))
        
        # padding
        payload += " " * (Util.get_message_size() - len(payload))
        return payload

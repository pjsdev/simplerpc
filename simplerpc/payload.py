import json

from util import Util

class Payload:
    @staticmethod
    def from_string(data):
        json_start = data.index("{")
        opcode = int(data[:json_start])
        json_string = data[json_start:]
        json_string = json_string.strip()
        args = json.loads(json_string)
        return (opcode, args)

    @staticmethod
    def to_string(opcode, args):
        # Note: no net_id is ever input into message
        payload = "{}{}".format(str(opcode), json.dumps(args))
        
        # padding
        payload += " " * (Util.get_message_size() - len(payload))
        return payload

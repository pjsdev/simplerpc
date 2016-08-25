import json

from exceptions import MalformedPayload
from config import Config

class Payload:
    """
    Namespace for payload encoding/decoding
    """

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
        """
        Return string representing a simplerpc message

        Raises:
            ValueError if we cannot convert opcode to string or
            parse JSON
        """
        # Note: no net_id is ever input into message
        payload = "{}{}".format(str(opcode), json.dumps(args))
        
        # padding
        payload += " " * (Config.get_message_size() - len(payload))
        return payload

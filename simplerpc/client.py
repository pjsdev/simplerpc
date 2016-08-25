from payload import Payload
from base_dispatcher import BaseDispatcher

from config import Config

class Client(BaseDispatcher):
    """
    Simple client to be subclassed
    Will connect and send on reads (as strings) to a handler

    also supplies the rpc function to allow opcode,args to be transmitted
    """
    def __init__(self, tcp_ip, tcp_port, handler):
        BaseDispatcher.__init__(self, tcp_ip, tcp_port, handler)

        self.message_size = None

        self.connect((tcp_ip, tcp_port))
        self.fail_callback = BaseDispatcher.nop

    def on_fail(self, func):
        if not callable(func):
            raise ValueError("Expected callable, got %s" % type(func))

        self.fail_callback = func

    def handle_connect(self):
        self.connect_callback()

    def handle_close(self):
        self.disconnect_callback()
        self.close()

    def handle_read(self):
        data = self.recv(Config.get_message_size())
        if data:
            opcode, data = Payload.from_string(data)
            if opcode == -1: # protocol FAIL
                self.fail_callback(data)
            elif opcode == -2: # protocol MESSAGE_SIZE
                self.message_size = int(data["message_size"])
            else:
                self.handler(self, opcode, data)
            
    def rpc(self, opcode, args):
        payload = Payload.to_string(opcode, args)
        self.send(payload)
from payload import Payload
from base_dispatcher import BaseDispatcher

from util import Util

class Client(BaseDispatcher):
    """
    Simple client to be subclassed
    Will connect and send on reads (as strings) to a handler

    also supplies the rpc function to allow opcode,args to be transmitted
    """
    def __init__(self, tcp_ip, tcp_port, handler):
        BaseDispatcher.__init__(self, tcp_ip, tcp_port, handler)

        self.connect((tcp_ip, tcp_port))

    def handle_connect(self):
        self.connect_callback()

    def handle_close(self):
        self.disconnect_callback()
        self.close()

    def handle_read(self):
        data = self.recv(Util.get_message_size())
        if data:
            rpc = Payload.from_string(data)
            self.handler(self, rpc[0], rpc[1])
            
    def rpc(self, opcode, args):
        payload = Payload.to_string(opcode, args)
        self.send(payload)
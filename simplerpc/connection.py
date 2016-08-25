import asyncore

from payload import Payload
from exceptions import RPCFailureException
from util import Util

class Connection(asyncore.dispatcher):
    def __init__(self, socket, net_id, handler):
        asyncore.dispatcher.__init__(self, socket)

        self.net_id = net_id
        self.handler = handler
        self.disconnect_callback = lambda: None

    def on_disconnect(self, func):
        self.disconnect_callback = func

    def handle_error(self):
        raise Util.asyncore_error()

    def handle_close(self):
        self.disconnect_callback()
        self.close()

    def handle_read(self):
        data = self.recv(Util.get_message_size())
        if data:
            try:
                rpc = Payload.from_string(data)
                self.handler(self, rpc[0], rpc[1])
            except RPCFailureException as e:
                data = {"reason": type(e).__name__, "message": e.message}
                self.rpc(-1, data)

    def rpc(self, opcode, args):
        payload = Payload.to_string(opcode, args)
        self.send(payload)
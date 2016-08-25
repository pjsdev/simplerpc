import asyncore

from payload import Payload
from exceptions import RPCFailureException
from config import Config

class Connection(asyncore.dispatcher):
    def __init__(self, socket, net_id, handler):
        asyncore.dispatcher.__init__(self, socket)

        self.net_id = net_id
        self.handler = handler
        self.disconnect_callback = lambda: None

        self.rpc(-2, {"message_size": Config.get_message_size()})        

    def on_disconnect(self, func):
        self.disconnect_callback = func

    def handle_error(self):
        # TODO: duplicate with BaseDispatcher
        nil, t, v, tbinfo = asyncore.compact_traceback()
        err = "---------- {} ------------\n {}\n{}\n -------------------".format(
            str(t),
            str(v), 
            "\n".join(tbinfo.split())
        )
        raise t(err)

    def handle_close(self):
        self.disconnect_callback()
        self.close()

    def handle_read(self):
        data = self.recv(Config.get_message_size())
        if data:
            try:
                opcode, data = Payload.from_string(data)
                self.handler(self, opcode, data)
            except RPCFailureException as e:
                data = {"reason": type(e).__name__, "message": e.message}
                self.rpc(-1, data)

    def rpc(self, opcode, args):
        payload = Payload.to_string(opcode, args)
        self.send(payload)
from .payload import Payload
from .base_dispatcher import BaseDispatcher

class Client(BaseDispatcher):
    """
    Simple client handling the simplerpc protocol opcodes
    and forward anything else onto handler

    Also has method rpc(opcode, data) to send rpc to server
    """
    def __init__(self, tcp_ip, tcp_port, handler):
        BaseDispatcher.__init__(self, tcp_ip, tcp_port, handler)

        self.connect((tcp_ip, tcp_port))
        self.decoder = Payload.BufferDecoder()
        self.response_callbacks = []

    def handle_connect(self):
        self.connect_callback()

    def handle_close(self):
        self.disconnect_callback()
        self.socket.close()

    def handle_read(self):
        buf = self.recv(1024)
        if not buf:
            print("Disconnect?")
            return

        for pkg in self.decoder.packages(buf):
            opcode, data = Payload.from_string(pkg)
            if opcode == "FAIL" or opcode == "OKAY":
                self.response_callbacks.pop()(self, opcode, data)

            self.handler(self, opcode, data)
        
    def rpc(self, opcode, args, cb=None):
        """
        Send simple rpc
        """
        callback = cb if cb else lambda conn,op,data: None

        self.response_callbacks.insert(0, callback)
        payload = Payload.to_string(opcode, args)
        self.send(payload.encode())
import asyncore

from exceptions import SimpleRPCException
from payload import Payload

class Connection(asyncore.dispatcher):
    """
    A connection created by the server when a client connects
    This is the endpoint for each client socket

    TODO(pjs): duplicate behaviour with BaseDispatcher

    This is responsible for sending out the simplerpc protocol 
    for FAIL protocol
    """
    def __init__(self, socket, net_id, handler):
        """
        Setup connection
        """
        asyncore.dispatcher.__init__(self, socket)

        self.net_id = net_id
        self.handler = handler
        self.disconnect_callback = lambda: None

        self.decoder = Payload.BufferDecoder()

        self.okay_data = {}

    def on_disconnect(self, func):
        self.disconnect_callback = func

    def handle_error(self):
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
        """
        Read the RPC from the socket, and hand of to the handler

        Catch all RPCFailureException objects for the FAIL rpc of the protocol
        """
        buf = self.recv(1024)
        if not buf:
            return

        for pkg in self.decoder.packages(buf):
            try:
                opcode, data = Payload.from_string(pkg)

                # send to our handler first, then the server level one
                self.handler(self, opcode, data)

                self.rpc("OKAY", self.okay_data)
                self.okay_data = {}

            except SimpleRPCException as e:
                data = {"reason": type(e).__name__, "message": e.message}
                self.rpc("FAIL", data)

            except Exception as e:
                data = {"reason": "Unknown", "message": "Uknown Server Error"}
                self.rpc("FAIL", data)
                raise e

                
    def rpc(self, opcode, args):
        """
        Send simplerpc
        """
        payload = Payload.to_string(opcode, args)
        self.send(payload)
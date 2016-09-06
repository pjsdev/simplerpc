import socket
from copy import copy

from .base_dispatcher import BaseDispatcher
from .connection import Connection

class Server(BaseDispatcher):
    """
    Server in charge of accepting connections and creating (and storing)
    Connection objects by net_id

    Each connection object is handed the servers handler on instantiation
    but this can be changed later

    The handler is never invoked directly from this class
    """
    def __init__(self, tcp_ip, tcp_port, handler):
        BaseDispatcher.__init__(self, tcp_ip, tcp_port, handler)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((tcp_ip, tcp_port))
        self.listen(1)

        self._connections = {}

    def connections(self):
        for conn in self._connections.values():
            yield conn

    # def rpc(self, net_id, opcode, args):
    #     """
    #     util method for sending rpc by net_id
    #     """
    #     if net_id not in self._connections:
    #         raise KeyError("Could not find net_id: %s " % net_id)

    #     self._connections[net_id].rpc(opcode, args)

    def rpc_all(self, opcode, args):
        """
        util method for sending rpc to all connections
        """
        for conn in self._connections.values():
            conn.rpc(opcode, args)

    def handle_accept(self):
        """
        Accept connection and set it up with servers handler
        Fire connect callback with connection object
        """
        socket, address = self.accept()
        net_id = hash(address)
        
        # we copy our handler configuration to the connection
        self._connections[net_id] = Connection(socket, net_id, copy(self.handler))
        self._connections[net_id].on_disconnect(lambda: self._disconnect(net_id))
        self.connect_callback(self._connections[net_id])

    def _disconnect(self, net_id):
        """
        Delete connection and fire disconnect_callback with net_id
        """
        if net_id in self._connections:
            self.disconnect_callback(self._connections[net_id])
            del self._connections[net_id]

    def handle_close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
import socket
import asyncore

from base_dispatcher import BaseDispatcher
from connection import Connection

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

        self.connections = {}

        print("TCP Server listening on %s:%s" % (tcp_ip, tcp_port))

    def rpc(self, net_id, opcode, args):
        """
        util method for sending rpc by net_id
        """
        if net_id not in self.connections:
            raise KeyError("Could not find net_id: %s " % net_id)

        self.connections[net_id].rpc(opcode, args)

    def rpc_all(self, opcode, args):
        """
        util method for sending rpc to all connections
        """
        for nid in self.connections.keys():
            self.rpc(nid, opcode, args)

    def handle_accept(self):
        """
        Accept connection and set it up with servers handler
        Fire connect callback with connection object
        """
        socket, address = self.accept()
        net_id = hash(address)
        
        self.connections[net_id] = Connection(socket, net_id, self.handler)
        self.connections[net_id].on_disconnect(lambda: self._disconnect(net_id))
        self.connect_callback(self.connections[net_id])

    def _disconnect(self, net_id):
        """
        Delete connection and fire disconnect_callback with net_id
        """
        if net_id in self.connections:
            del self.connections[net_id]

        self.disconnect_callback(net_id)

    def handle_close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
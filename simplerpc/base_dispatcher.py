import socket
import asyncore

from util import Util

class BaseDispatcher(asyncore.dispatcher):

    @staticmethod
    def nop(*args, **kwargs):
        pass

    def __init__(self, tcp_ip, tcp_port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.msg_table = {}

        self.connect_callback = BaseDispatcher.nop
        self.disconnect_callback = BaseDispatcher.nop
  
    def on_connect(self, func):
        if not callable(func):
            raise ValueError("Expected Callable, got %s" % type(func))

        self.connect_callback = func

    def on_disconnect(self, func):
        if not callable(func):
            raise ValueError("Expected Callable, got %s" % type(func))

        self.disconnect_callback = func

    def bind(self, msg, func):
        if msg in self.msg_table:
            print("WARNING: Overriding message %s" % msg)

        self.msg_table[msg] = func

    def unbind(self, msg):
        if msg in self.msg_table:
            del self.msg_table[msg]

    def unbind_all(self):
        self.msg_table = {}

    def start(self):
        asyncore.loop()

    def handle_error(self):
        raise Util.asyncore_error()


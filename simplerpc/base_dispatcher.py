import socket
import asyncore

from util import Util

class BaseDispatcher(asyncore.dispatcher):

    @staticmethod
    def nop(*args, **kwargs):
        pass

    def __init__(self, tcp_ip, tcp_port, handler):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.handler = handler

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

    def start(self):
        asyncore.loop()

    def handle_error(self):
        raise Util.asyncore_error()


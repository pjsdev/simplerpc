import socket
import asyncore

from config import Config

class BaseDispatcher(asyncore.dispatcher):
    """
    Internal class for some common socket behaviour, including error handling
    and on_connect, on_disconnect callback registering
    """
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
        Config.lock = True
        asyncore.loop()

    def handle_error(self):
        nil, t, v, tbinfo = asyncore.compact_traceback()
        err = "---------- {} ------------\n {}\n{}\n -------------------".format(
            str(t),
            str(v), 
            "\n".join(tbinfo.split())
        )
        raise t(err)


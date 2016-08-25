from base_handler import BaseHandler

class ForwardHandler(BaseHandler):
    """
    Handler to forward RPC to all listeners
    """
    def __init__(self):
        self.callbacks = []

    def listen(self, func):
        """
        Add a callback to be called when a message is received
        """
        if not callable(func):
            raise ValueError("Expected callable, got %s" % type(func))

        self.callbacks.append(func)

    def clear_all(self):
        self.callbacks = []

    def clear(self, func):
        if func in self.callbacks:
            self.callable.remove(func)

    def __call__(self, conn, opcode, data):
        for cb in self.callbacks:
            cb(conn, opcode, data)
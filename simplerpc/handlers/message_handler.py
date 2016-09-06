from .base_handler import BaseHandler

class MessageHandler(BaseHandler):
    """
    Handler to forward RPCs, by opcode, to all listeners
    """
    def __init__(self):
        self.msg_table = {}

    def on(self, opcode, func):
        """
        Register callback for given opcode
        """
        if not callable(func):
            raise ValueError("Expected callable, got %s" % type(func))

        if opcode not in self.msg_table:
            self.msg_table[opcode] = []

        self.msg_table[opcode].append(func)

    def clear(self, opcode):
        """
        Remove callbacks currently registered for opcode
        """
        if opcode in self.msg_table:
            del self.msg_table[opcode]

    def clear_all(self):
        """
        Clear all callbacks
        """
        self.msg_table = {}

    def __call__(self, conn, opcode, data):
        """
        Call relevant callback for this opcode
        """
        if opcode in self.msg_table:
            for cb in self.msg_table[opcode]:
                cb(conn, data)

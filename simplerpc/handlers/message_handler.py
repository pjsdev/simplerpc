from base_handler import BaseHandler

class MessageHandler(BaseHandler):
    def __init__(self):
        self.msg_table = {}

    def on(self, msg, func):
        if msg in self.msg_table:
            print("WARNING: Overriding message %s" % msg)

        self.msg_table[msg] = func

    def clear(self, msg):
        if msg in self.msg_table:
            del self.msg_table[msg]

    def clear_all(self):
        self.msg_table = {}

    def __call__(self, conn, opcode, data):
        if opcode in self.msg_table:
            self.msg_table[opcode](conn, data)

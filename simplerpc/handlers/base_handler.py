class BaseHandler(object):
    """
    The base class for implementing a handler
    for the simplerpc protocol

    Protocol opcodes are handled internally, this class
    will just get the application opcodes
    """
    def __call__(self, conn, opcode, args):
        raise NotImplementedError

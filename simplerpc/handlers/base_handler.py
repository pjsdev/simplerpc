class BaseHandler(object):
    def __call__(self, conn, opcode, args):
        raise NotImplementedError

class RPCFailureException(Exception):
    pass

class ArgumentTypeError(RPCFailureException):
    pass

class ArgumentValueError(RPCFailureException):
    pass

class ArgumentMissing(RPCFailureException):
    pass

class MalformedPayload(RPCFailureException):
    pass
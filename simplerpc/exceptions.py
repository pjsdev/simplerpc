class RPCFailureException(Exception):
    """
    Base class for all exceptions to be caught as
    part of the FAIL protocl of simplerpc 
    """
    pass

class ArgumentTypeError(RPCFailureException):
    pass

class ArgumentValueError(RPCFailureException):
    pass

class ArgumentMissing(RPCFailureException):
    pass

class MalformedPayload(RPCFailureException):
    pass
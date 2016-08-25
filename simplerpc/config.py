import asyncore

# TODO(pjs): move this to the base of the module
class Config:
    """
    Basic config object to be setup before starting server
    """
    message_size = 1024
    lock = False

    @staticmethod
    def set_message_size(size):
        if not Config.lock:
            Config.message_size = size
        else:
            print("ERROR: cannot alter config after lock")

    @staticmethod
    def get_message_size():
        return Config.message_size
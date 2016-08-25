import asyncore

# TODO(pjs): move this to the base of the module
class Config:
    message_size = 1024

    @staticmethod
    def set_message_size(size):
        Config.message_size = size

    @staticmethod
    def get_message_size():
        return Config.message_size
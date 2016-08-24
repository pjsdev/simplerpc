import asyncore

# TODO(pjs): move this to the base of the module
class Util:
    message_size = None

    @staticmethod
    def asyncore_error():
        nil, t, v, tbinfo = asyncore.compact_traceback()
        err = "---------- {} ------------\n {}\n{}\n -------------------".format(
            str(t),
            str(v), 
            "\n".join(tbinfo.split())
        )
        return t(err)

    @staticmethod
    def set_message_size(size):
        Util.message_size = size

    @staticmethod
    def get_message_size():
        return Util.message_size
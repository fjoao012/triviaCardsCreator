import os


class Utils:
    @staticmethod
    def is_valid_file_with_extension(parser, arg, extension):
        if not arg.endswith(extension):
            parser.error("The file does not end with " + extension % arg)
        else:
            return arg

    @staticmethod
    def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            # return an open file handle
            return open(arg, mode="r", encoding="utf-8")

    @staticmethod
    def is_valid_folder(parser, arg):
        if not os.path.exists(arg) or not os.path.isdir(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            # return an open file handle
            return arg

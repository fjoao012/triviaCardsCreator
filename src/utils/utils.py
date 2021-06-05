import os
import random


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

    @staticmethod
    def get_random_number(min_value, max_value):
        return random.randint(min_value, max_value)

    @staticmethod
    def rename_all_files_in_folder(path, output_base_name):
        files = os.listdir(path)
        for index, file in enumerate(files):
            ending = "." + file.split(".")[-1]
            os.rename(os.path.join(path, file),
                      os.path.join(path, ''.join([output_base_name, str(index),
                                                  ending])))

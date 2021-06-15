import argparse
import re

from utils.utils import Utils

marker = "XX"
pattern = re.compile(r"question([0-9]{3})")


def parse_arguments():
    global marker

    parser = argparse.ArgumentParser()
    q_help = "JSON containing a set of questions with incorrect numbering"
    parser.add_argument("-q", "--questions", help=q_help, required=True,
                        type=lambda x: Utils.is_valid_file(parser, x))
    o_help = "Output file with the corrected question numbers"
    parser.add_argument("-o", "--output", help=o_help, required=True,
                    type=str)
    return parser.parse_args()


def write_list_into_open_file_handler(line_list, file_handler):
    for line in line_list:
        file_handler.write(line)


def replace_question_numbers(lines):
    counter = 0
    out_lines = []
    for line in lines:
        if "question" in line:
            out_lines.extend([
                pattern.sub("question"+str(f"{counter:03d}"), line)])
            counter += 1
        else:
            out_lines.extend([line])
    return out_lines


if __name__ == "__main__":
    args = parse_arguments()
    output_file = open(args.output, 'w', encoding="utf-8")
    interm_lines = [line for line in args.questions]

    out_lines = replace_question_numbers(interm_lines)
    write_list_into_open_file_handler(out_lines, output_file)


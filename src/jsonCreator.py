import argparse
import json
import os.path


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        # return an open file handle
        return open(arg, mode="r", encoding="utf-8")


def is_valid_json(parser, arg):
    if not arg.endswith(".json"):
        parser.error("The file does not end with .json" % arg)
    else:
        return arg


def parse_arguments():
    parser = argparse.ArgumentParser()
    q_help = "File containing a set of questions in simple text to create the "\
             "trivia cards"
    parser.add_argument("-q", "--questions", help=q_help, required=True,
                        type=lambda x: is_valid_file(parser, x))
    o_help = "Output JSON file with the same set of questions"
    parser.add_argument("-o", "--output", help=o_help, required=True,
                    type=lambda x: is_valid_json(parser, x))
    return parser.parse_args()


def prepare_json_structure(question_list):
    my_map = {}
    for index, q in enumerate(question_list):
        q_map = {"q": q, "a": ["", "", "", ""]}
        my_map["question" + str(f"{index:03d}")] = q_map
    return my_map


def write_json_to_file(json_structure, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_structure, f, sort_keys=True, indent=4,
                  ensure_ascii=False)


if __name__ == "__main__":
    args = parse_arguments()
    questions = [line.rstrip('\n') for line in args.questions]
    json_structure = prepare_json_structure(questions)
    write_json_to_file(json_structure, args.output)

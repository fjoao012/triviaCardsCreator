import argparse
import os.path


marker = "XX"


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        # return an open file handle
        return open(arg, mode="r", encoding="utf-8")  


def parse_arguments():
    global marker

    parser = argparse.ArgumentParser()
    q_help = "File containing a set of questions with " + marker + \
             " as replacing element"
    parser.add_argument("-q", "--questions", help=q_help, required=True,
                        type=lambda x: is_valid_file(parser, x))
    p_help = "File containing people's names (including personal pronoun)" +\
             " to replace in each question, at " + marker
    parser.add_argument("-p", "--people", help=p_help, required=True,
                        type=lambda x: is_valid_file(parser, x))
    o_help = "Output file with the unfolded questions"
    parser.add_argument("-o", "--output", help=o_help, required=True,
                    type=str)
    return parser.parse_args()


def unfold_question_with_people(question, people):
    global marker

    out_list = []
    for person in people:
        q = question.replace(marker, person)
        out_list.append(q)
    return out_list


def unfold_all_questions(questions_file_handler, people_list):
    global marker

    for q_line in questions_file_handler:
        if marker in q_line:
            current_list = unfold_question_with_people(q_line, people_list)
        else:
            current_list = [q_line]
        write_list_into_open_file_handler(current_list, output_file)


def write_list_into_open_file_handler(line_list, file_handler):
    for line in line_list:
        file_handler.write(line)


if __name__ == "__main__":
    args = parse_arguments()
    output_file = open(args.output, 'w', encoding="utf-8")
    people = [line.rstrip('\n') for line in args.people if "#" not in line]
    unfold_all_questions(args.questions, people)


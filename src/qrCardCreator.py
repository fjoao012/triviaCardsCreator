import argparse
import math
import shutil
import textwrap
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool
from os import listdir
from os.path import isfile, join
from pathlib import Path
from utils.utils import Utils

placeholder = "XX"
input_extension = ".emf"
output_extension = ".png"
input_image_name_template = "../resources/images/special_card_" + placeholder\
                            + \
                            input_extension
output_image_name_template = input_image_name_template.replace(
    input_extension, output_extension).replace("resources/images", "output_qr")


def parse_arguments():
    parser = argparse.ArgumentParser()
    q_help = "File containing a set of questions in JSON format to create the " \
             "" \
             "trivia cards"
    parser.add_argument("-q", "--questions", help=q_help, required=True,
                        type=lambda x: Utils.is_valid_file(parser,
                                                           Utils.is_valid_file_with_extension(
                                                               parser, x,
                                                               ".txt")))
    c_help = "Folder containing the QR codes (as images) to create the " \
             "trivia cards"
    parser.add_argument("-c", "--qrcodes", help=c_help, required=True,
                        type=lambda x: Utils.is_valid_folder(parser, x))
    return parser.parse_args()


def draw_question_text(draw, font, question, initial_x, initial_y):
    lines = textwrap.wrap(question, width=30)
    y_text = initial_y
    _, line_height = font.getsize("bpQ")  # I want a fixed line height
    for line in lines:
        draw.text((initial_x, y_text), text=line, font=font, fill="black",
                  anchor="la")
        y_text += (math.ceil(line_height * 1.2))


def paste_qr_code(image, qr_code):
    qr_code_image = Image.open(qr_code).resize((1500, 1500))
    image.paste(qr_code_image, (880, 2190))


def delete_and_recreate_folder(image_name):
    folder_path = Path(image_name).parent
    try:
        shutil.rmtree(folder_path)
    except FileNotFoundError:
        print("Output file was not found. Continuing")
    folder_path.mkdir(parents=True, exist_ok=True)


def save_image(image, image_name):
    image.save(image_name)


def draw_card(question, qr_code, question_number):
    global placeholder, input_extension, output_extension, \
        input_image_name_template, output_image_name_template

    number = str(Utils.get_random_number(1, 3))
    input_image_name = input_image_name_template.replace(placeholder, number)
    output_image_name = output_image_name_template.replace(placeholder,
                                                           question_number)

    image = Image.open(input_image_name)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 190)
    draw = ImageDraw.Draw(image)

    # write the question
    draw_question_text(draw, font, question, 250, 300)

    # write the answers
    paste_qr_code(image, qr_code)

    save_image(image, output_image_name)


if __name__ == "__main__":
    args = parse_arguments()

    questions = [line.rstrip('\n') for line in args.questions]

    # Utils.rename_all_files_in_folder(args.qrcodes, "qr_")

    qr_codes = ["../resources/qr_codes/" + f for f in listdir(args.qrcodes) if
                isfile(join(args.qrcodes, f))]
    if len(questions) < len(qr_codes):
        questions.extend([questions[-1]] * (len(qr_codes) - len(questions)))

    my_list = [(p1, p2, str(idx1)) for idx1, p1 in enumerate(questions)
               for idx2, p2 in enumerate(qr_codes) if idx1 == idx2]

    delete_and_recreate_folder(output_image_name_template)
    with Pool(6) as p:
        p.starmap(draw_card, my_list)
    print("THE END")

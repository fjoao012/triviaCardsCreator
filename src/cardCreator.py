import argparse
import json
import math
import random
import shutil
import textwrap
from multiprocessing import Pool
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from utils.utils import Utils

placeholder = "XX"
input_extension = ".emf"
output_extension = ".png"
input_image_name_template = "../resources/images/quiz_card_" + placeholder + \
                            input_extension
output_image_name_template = input_image_name_template.replace(
    input_extension, output_extension).replace("resources/images", "output")


def parse_arguments():
    parser = argparse.ArgumentParser()
    q_help = "File containing a set of questions in JSON format to create the "\
             "trivia cards"
    parser.add_argument("-q", "--questions", help=q_help, required=True,
                        type=lambda x: Utils.is_valid_file(parser,
                                                           Utils.is_valid_file_with_extension(
                                                               parser, x,
                                                               ".json")))
    return parser.parse_args()


def get_random_number(min_value, max_value):
    return random.randint(min_value, max_value)


def draw_question_text(draw, font, question, initial_x, initial_y):
    lines = textwrap.wrap(question, width=30)
    y_text = initial_y
    _, line_height = font.getsize("bpQ")  # I want a fixed line height
    for line in lines:
        draw.text((initial_x, y_text), text=line, font=font, fill="black",
                  anchor="la")
        y_text += (math.ceil(line_height * 1.2))


def draw_answers_text(draw, font, answers, initial_x, initial_y):
    y_text = initial_y
    line_increment = 490  # fixed
    for line in answers:
        draw.text((initial_x, y_text), text=line, font=font, fill="black",
                  anchor="la")
        y_text += line_increment


def delete_and_recreate_folder(image_name):
    folder_path = Path(image_name).parent
    try:
        shutil.rmtree(folder_path)
    except FileNotFoundError:
        print("Output file was not found. Continuing")
    folder_path.mkdir(parents=True, exist_ok=True)


def save_image(image, image_name):
    image.save(image_name)


def draw_card(question, answers, question_number):
    global placeholder, input_extension, output_extension, \
        input_image_name_template, output_image_name_template

    number = str(get_random_number(1, 7))
    input_image_name = input_image_name_template.replace(placeholder, number)
    output_image_name = output_image_name_template.replace(placeholder,
                                                           question_number)

    image = Image.open(input_image_name)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 190)
    draw = ImageDraw.Draw(image)

    # write the question
    draw_question_text(draw, font, question, 250, 300)

    # write the answers
    draw_answers_text(draw, font, answers, 720, 2080)

    save_image(image, output_image_name)


if __name__ == "__main__":
    args = parse_arguments()

    question_set = json.load(args.questions)
    my_list = [(v["q"], v["a"], str(i)) for i, (k, v) in enumerate(
        question_set.items())]

    delete_and_recreate_folder(output_image_name_template)
    with Pool(6) as p:
        p.starmap(draw_card, my_list)
    print("THE END")

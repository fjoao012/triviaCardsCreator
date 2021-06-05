import argparse
import os

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Cm
from utils.utils import Utils


def parse_arguments():
    parser = argparse.ArgumentParser()
    c_help = "Folder containing the cards to print in PNG format"
    parser.add_argument("-c", "--cards", help=c_help, required=True,
                        type=lambda x: Utils.is_valid_folder(parser, x))
    o_help = "Output DOCX file with all images inside, ready to print"
    parser.add_argument("-o", "--output", help=o_help, required=True,
                        type=lambda x: Utils.is_valid_file_with_extension(
                            parser, x, ".docx"))
    return parser.parse_args()


def create_document():
    document = Document()
    section = document.sections[-1]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.left_margin = Cm(1)
    section.right_margin = Cm(1)
    section.top_margin = Cm(1)
    section.bottom_margin = Cm(1)
    return document


def add_all_images_to_document(document, images_location, output_file):
    for filename in os.listdir(images_location):
        if filename.endswith(".png"):
            pic_path = os.path.abspath(images_location + "/" + filename)
            document.add_picture(pic_path, width=Cm(7.5))
    document.save(output_file)


if __name__ == "__main__":
    args = parse_arguments()
    document = create_document()
    add_all_images_to_document(document, args.cards, args.output)

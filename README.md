# triviaCardsCreator
Python app that creates trivia cards based on the questions that are fed.

## Requirements
- Python 3.9  

## Description
This repository contains three python scripts:
- `questionUnfolder.py`
- `jsonCreator.py`
- `cardCreator.py`

That shall be used in this order.  

#### `questionUnfolder.py`
This script takes a set of questions and a set of names and unfold the questions with the names given.  
In case a question does not have a marker, then the question is transposed to the output without any
unfolding.

It takes 3 arguments, which shall all be ".txt" files:

- `-q` questions file: a file containing questions, separated by a newline. The questions might have
a placeholder in case we have a list of people to apply those questions to (see argument `-p`).
- `-p` people file: a file containing people names, separated by a newline.
In case a new line starts with `#`, then that line (i.e. that name) is ignored.
- `-o` output file: file name where the unfolded questions will be written.

The output file of this script will be the input file of the next script.

#### `jsonCreator.py`
This script just translates the questions file (in .txt format) into a JSON file (for easier manual 
editing and parsing).
 
It takes 2 arguments, being the input a ".txt" file and the output a ".json" file:

- `-q` questions file: a file containing all the questions, separated by a newline.
- `-o` output file: file name where the unfolded questions will be written, in JSON format.

The output file of this script will be the input file of the next script.

#### `cardCreator.py`
This script just translates a JSON file (with a predefined format) trivia cards.  
This process is done
by grabbing all the information on the JSON, selecting random empty cards from the `resources/images/`
folder and filling the spaces. 
 
It takes 1 argument, which is the ".json" file:

- `-q` questions file: a JSON file containing all the questions.

The script will create as many cards as questions, and will write them as PNG images into the `output/`
folder.  

**NOTE:** this script uses a TrueType font, whose location is hardcoded (Arial @Windows 10). Please
change that in case you're not running this under Windows and/or want a different font. 
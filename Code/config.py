""" A Configuration file with the value of the project Root """

import os.path

CODE_DIR = os.path.dirname(__file__)
ROOT = os.path.split(CODE_DIR)[0]

print("This is the ROOT", ROOT)
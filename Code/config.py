""" A Configuration file with the value of the project Root """

import os.path

CONFIG_DIR = os.path.dirname(__file__)
ROOT = os.path.split(CONFIG_DIR)[0]

print("This is the ROOT", ROOT)
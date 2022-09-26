"""
Testing feature set robustness creating several instances of existing MIDIs with added noise
"""

import config

import sys

import random

from MIDI_add_noise import add_noise_batch_multiple_instances

if __name__ == "__main__":
# Adding noise to several files
    # Make the output be in a folder "Noise_added"

    files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

    PERCENTAGE = 0.2
    MAX_DEVIATION = 5
    NUM_INSTANCES = 10

    ## To input Percentage and Max deviation as command line input
    # if len(sys.argv) == 2:
    #     percentage = 0.1
    #     max_deviation = 5

    # else:
    #     percentage = float(sys.argv[2])
    #     max_deviation = int(sys.argv[3])

    random.seed(42)

    add_noise_batch_multiple_instances(files_directory, PERCENTAGE, MAX_DEVIATION, num_instances = NUM_INSTANCES)


import networkx as nx
import mido
import sys
import os.path
from os import listdir
import Plotting





if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]
    files_directory = parent_directory + "\\SongArena" # Where the MIDI files to be compared are

    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

    # Create the Graphs
    for mid in list_files:
        pass



    # SongComparisonOutputFiles
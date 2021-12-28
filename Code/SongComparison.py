import networkx as nx
import mido
import sys
import os.path
from os import listdir
import Plotting
import MIDI_general
import Music_Mapping



if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]
    files_directory = parent_directory + "\\SongArena" # Where the MIDI files to be compared are

    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

    # Create the Graphs
    networks = []
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)
    
        # Graph creation
        note_pairs = Music_Mapping.get_note_pairs(mid_file)
        network = Music_Mapping.graph_note_interval(note_pairs)

        filename = MIDI_general.midi_filename(mid_file)
        networks.append([network, mid_file, filename])


    # Plot the Degree Distribution Scatterplot
    Plotting.DegreeDistributionComparison(networks)
    Plotting.DegreeDistributionComparisonLogLog(networks)

    # SongComparisonOutputFiles
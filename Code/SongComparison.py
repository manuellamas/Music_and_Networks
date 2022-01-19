import networkx as nx
import mido

import sys
import os.path
from os import listdir
from tabulate import tabulate

import Plotting
import MIDI_general
import Music_Mapping





if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]

    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena")
        files_directory = parent_directory + "\\SongArena" # Where the MIDI files to be compared are
        plot_folder = "SongArena"
    elif len(sys.argv) == 2:
        files_directory = parent_directory + "\\" + sys.argv[-1] # Where the MIDI files are
        plot_folder = sys.argv[-1]
        group_name = ""
        for i in range(len(plot_folder)):
            if plot_folder[-1-i] == "\\":
                break
            else:
                group_name += plot_folder[-1-i]
        group_name = group_name[::-1]


    else:
        print("Too many arguments")






    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

    # Create the Graphs
    networks = []
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        network, notes = Music_Mapping.graph_note_pairs_weighted(mid_file)
        filename = MIDI_general.midi_filename(mid_file)

        networks.append([network, mid_file, filename, notes])


    ########## Plots ##########
    # Degree Distribution
    Plotting.degree_distribution_comparison_plot(networks, plot_folder = group_name)
    Plotting.degree_distribution_comparison_plot(networks, scale = "loglog", plot_folder = group_name)
    
    # Betweenness and Closeness
    Plotting.betwenness_comparison_plot(networks, plot_folder = group_name)
    Plotting.closeness_comparison_plot(networks, plot_folder = group_name)

    # Clustering Coefficient
    Plotting.clustering_coef_comparison_plot(networks, plot_folder = group_name)

    # Edges Rank
    

    # Diameter
    diameters = []

    # Data Formatting
    data = []
    headers = ["Song", "Diameter", "Length of track (#nodes)"]
    for network, mid_file, filename, notes in networks:
        diameter = nx.diameter(network)
        data.append([filename, diameter, len(notes)])

    print(tabulate(data, headers = headers))

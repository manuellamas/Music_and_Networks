import networkx as nx
import mido

import sys

from os import listdir
import os.path
from tabulate import tabulate

import config
import Plot.Plotting_Song_Comparison as plt_comparison
import MIDI_general
import Music_Mapping




if __name__ == "__main__":
    group_name = None # Default value

    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena")
        files_directory = config.ROOT + "\\SongArena" # Where the MIDI files to be compared are
        group_name = "SongArena"
    elif len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are
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
        exit()






    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

    if len(list_files) == 0:
        print("The folder is empty")
        exit()

    # Create the Graphs
    networks = []
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        network, notes = Music_Mapping.graph_note_pairs_weighted(mid_file)
        filename = MIDI_general.midi_filename(mid_file)

        networks.append([network, mid_file, filename, notes])


    ########## Plots ##########
    # Degree Distribution
    plt_comparison.degree_distribution_comparison_plot(networks, plot_folder = group_name)
    plt_comparison.degree_distribution_comparison_plot(networks, scale = "loglog", plot_folder = group_name)
    
    # Betweenness and Closeness
    plt_comparison.betwenness_comparison_plot(networks, plot_folder = group_name)
    plt_comparison.betwenness_comparison_plot_sides(networks, plot_folder = group_name)
    plt_comparison.closeness_comparison_plot(networks, plot_folder = group_name)

    # Clustering Coefficient
    plt_comparison.clustering_coef_comparison_plot(networks, plot_folder = group_name)

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

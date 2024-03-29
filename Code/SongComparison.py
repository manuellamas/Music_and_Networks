import networkx as nx
import mido

import sys

from os import listdir
import os.path
from tabulate import tabulate

import config
import Plot.Plotting_Song_Comparison as plt_comparison
from Plotting import check_dir
import MIDI_general
import Music_Mapping





def main_song_comparison_plots(files_directory, full_analysis = True):
    # Create the Graphs
    tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand

    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

    if len(list_files) == 0:
        print("The folder is empty")
        exit()
    else:
        print("Looking into the files", list_files)

    networks = []
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        filename = MIDI_general.midi_filename(mid_file)
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)
        network, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file, track_index = track_index)

        networks.append([network, mid_file, filename, notes])


    ########## Plots ##########
    # Creating directory for group if it doesn't already exist
    if not full_analysis:
        path = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name
    else:
        path = files_directory + "\\SongGroupAnalysis\\Comparison"
    check_dir(path)

    # Degree Distribution
    plt_comparison.degree_distribution_comparison_plot(networks, files_directory = files_directory)
    plt_comparison.degree_distribution_comparison_plot(networks, scale = "loglog", files_directory = files_directory)
    
    # Betweenness and Closeness
    plt_comparison.betwenness_comparison_plot(networks, files_directory = files_directory)
    plt_comparison.betwenness_comparison_plot_sides(networks, files_directory = files_directory)
    plt_comparison.closeness_comparison_plot(networks, files_directory = files_directory)

    # Clustering Coefficient
    plt_comparison.clustering_coef_comparison_plot(networks, files_directory = files_directory)

    # Edges Rank
    plt_comparison.edges_rank_comparison(networks, files_directory = files_directory)

    return networks



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





    networks = main_song_comparison_plots(files_directory)



    # # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    # list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

    # if len(list_files) == 0:
    #     print("The folder is empty")
    #     exit()
    # else:
    #     print("Looking into the files", list_files)

    # # Create the Graphs
    # tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
    
    # networks = []
    # for mid in list_files:
    #     mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

    #     filename = MIDI_general.midi_filename(mid_file)
    #     track_index = MIDI_general.track_from_dict(filename, tracks_indices)
    #     network, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file, track_index = track_index)

    #     networks.append([network, mid_file, filename, notes])


    # ########## Plots ##########
    # # Creating directory for group if it doesn't already exist
    # path = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name
    # check_dir(path)

    # # Degree Distribution
    # plt_comparison.degree_distribution_comparison_plot(networks, plot_folder = group_name)
    # plt_comparison.degree_distribution_comparison_plot(networks, scale = "loglog", plot_folder = group_name)
    
    # # Betweenness and Closeness
    # plt_comparison.betwenness_comparison_plot(networks, plot_folder = group_name)
    # plt_comparison.betwenness_comparison_plot_sides(networks, plot_folder = group_name)
    # plt_comparison.closeness_comparison_plot(networks, plot_folder = group_name)

    # # Clustering Coefficient
    # plt_comparison.clustering_coef_comparison_plot(networks, plot_folder = group_name)

    # # Edges Rank
    # plt_comparison.edges_rank_comparison(networks, plot_folder = group_name)




    # Command Line Table print
    # Diameter
    diameters = []

    # Data Formatting
    data = []
    headers = ["Song", "Diameter", "Length of track (#nodes)"]
    for network, mid_file, filename, notes in networks:
        diameter = nx.diameter(network)
        data.append([filename, diameter, len(notes)])

    print(tabulate(data, headers = headers))

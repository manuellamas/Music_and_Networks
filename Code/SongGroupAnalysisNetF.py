""" Analyze several songs by obtaining its NetF features """

import sys
import config
import os.path
from os import listdir

import mido
import networkx as nx

import Music_Mapping
import MIDI_general
import Plot.Plotting_Group_Analysis as plt_analysis
import MIDITimeSeries

from SongGroupAnalysis import *











if __name__ == "__main__":

    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena")
        files_directory = config.ROOT + "\\SongArena" # Where the MIDI files to be analyzed are
        group_name = "SongArena"

    elif len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are
        group_name = sys.argv[-1].rsplit('\\', 1)[-1] # Used to denote the folder

    else:
        print("Too many arguments")
        exit()

    import time
    start_time = time.time()

    # Obtain a list of the file names of all MIDI files in the directory (SongArena by Default). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

    if len(list_files) == 0:
        print("The folder is empty")
        exit()

    print("Running for the following files:")
    for mid in list_files:
        print(mid)

    # Create the Graphs
    networks = []
    tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand

    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        track_index = MIDI_general.track_from_dict(filename, tracks_indices)
        filename = MIDI_general.midi_filename(mid_file)

        network, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file, track_index = track_index)

        nx.write_graphml(network, config.ROOT + "\\graphml_files\\" + filename + "_Graph.graphml") # Exporting graph to a graphml file
        network = nx.relabel_nodes(network, MIDI_general.note_mapping_dict(network)) # Adding labels according to the notes

        networks.append([network, mid_file, filename, notes])






    #################
    # NetF Features #
    #################

    netf_feature_list = [] # Each entry is relative to a song

    # Running the Rscript only once
    filenames = []
    networks_midi_files = []
    for i in range(len(networks)):
        networks_midi_files.append(networks[i][1]) # Storing the mid_files (objects)
        filenames.append(networks[i][2]) # Saving the filenames
    netf_all_series_strings = MIDITimeSeries.features_from_MIDI_series_group(networks_midi_files, num_quantiles = 8)


    for i in range(len(networks)):
        netf_strings = netf_all_series_strings[i] # Getting the net features for midi file i
        netf_float = []
        for i in range(len(netf_strings)):
            netf_float.append(float(netf_strings[i])) # Converting to float and appending all to a single list
        netf_feature_list.append(netf_float) # Each entry is a list with the netf features of a midi file


    # # Running the Rscript once per file
    # filenames = []
    # for i in range(len(networks)):
    #     filenames.append(networks[i][2])

    #     # Converting the values, that came as strings from the CSV, to floats
    #     netf_strings = MIDITimeSeries.series_from_MIDI(networks[i][1])
    #     netf_float = []
    #     for i in range(len(netf_strings)):
    #         netf_float.append(float(netf_strings[i]))
    #     netf_feature_list.append(netf_float)

    # NetF Feature Table
    netf_feature_names = ["Song", "NVG - k", "NVG - d", "NVG - S", "NVG - C", "NVG - Q", "HVG - k" , "HVG - d", "HVG - S", "HVG - C", "HVG - Q", "QG - k", "QG - d", "QG - S", "QG - C", "QG - Q"]
    # plt_analysis.feature_table(netf_feature_list, netf_feature_names, filenames, group_name, type = "netf")




    ###################
    # NetF Clustering #
    ###################

    # k-means
    kmean_predictions = kmeans_analysis(netf_feature_list)
    # plt_analysis.clustering_table(networks, kmean_predictions, "netf_k-means", group_name) # Just the clustering without the features values
    plt_analysis.cluster_feature_table(networks, kmean_predictions, "netf_k-means", netf_feature_list, netf_feature_names, filenames, group_name = group_name)

    # DBSCAN
    # dbscan_predictions = dbscan_analysis(netf_feature_list)
    # plt_analysis.clustering_table(networks, dbscan_predictions,"netf_DBSCAN", group_name)




    print("\n\n----- %s seconds -----" % (time.time() - start_time))
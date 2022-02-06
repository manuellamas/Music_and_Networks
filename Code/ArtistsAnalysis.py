import sys
import config

import os.path
from os import listdir

import mido
import networkx as nx

import Music_Mapping
import MIDI_general
import Plot.Plotting_Group_Analysis as plt_analysis
import SongGroupAnalysis as song_analysis


if __name__ == "__main__":

    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena\Artist Analysis")
        files_directory = config.ROOT + "\\SongArena\\Artist_Analysis" # Where the MIDI files to be analyzed are

    elif len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

    else:
        print("Too many arguments")
        exit()

    # Checking if the directory has only two folders, if it has it assumes it's to distinguish each folder as an artist/band
    list_folders = [f for f in listdir(files_directory) if os.path.isdir(os.path.join(files_directory, f))]
    if len(list_folders) != 2:
        print("The chosen directory doesn't have (exactly) 2 folders")
        exit()
    else:
        print("Looking into the folders", list_folders)


    dirs = []
    for i in range(len(list_folders)):
        dirs.append(files_directory + "\\" + list_folders[i])

    # Getting midi files for each artist/band
    list_files = []
    for i in range(len(list_folders)):
        list_files.append([f for f in listdir(dirs[i]) if (os.path.isfile(os.path.join(dirs[i], f)) and f[-3:]) == "mid"])

        if len(list_files[i]) == 0:
            print("The folder '" + list_folders[i] + "' is empty")
            exit()

    # Create the Graphs
    networks = []
    labels = [] # To distinguish each artist/band on plots
    for i in range(len(list_files)):
        label = list_folders[i]
        for mid in list_files[i]:
            mid_file = mido.MidiFile(dirs[i] + "\\" + mid, clip = True)

            network, notes = Music_Mapping.graph_note_pairs_weighted(mid_file)
            filename = MIDI_general.midi_filename(mid_file)

            networks.append([network, mid_file, filename, notes])
            labels.append(label)

    # Feature List
    networks_feature_list = []
    for network, mid_file, filename, notes in networks:
        time_length = 0
        try:
            time_length = mid_file.length
        except:
            print("This MIDI file is of type 2 (asynchronous) and so the length can't be computed")
            print("This song '" + filename + "'should probably be removed, or the analysis done without the length")

        if time_length == 0:
            networks_feature_list.append(song_analysis.music_data(network, 0))
        else:
            networks_feature_list.append(song_analysis.music_data(network, len(notes)/time_length))


    # k-means
    kmean_predictions = song_analysis.kmeans_analysis(networks_feature_list)
    plt_analysis.clustering_table(networks, kmean_predictions, "k-means", labels)

    # DBSCAN
    dbscan_predictions = song_analysis.dbscan_analysis(networks_feature_list)
    print(len(dbscan_predictions))
    plt_analysis.clustering_table(networks, dbscan_predictions, "DBSCAN", labels)
""" Display the values of a set of Features (metrics) on a dataset of MIDI files """


import sys
import os.path
from os import listdir

import config

import networkx as nx
import mido

import Music_Mapping
import MIDI_general
import Graph_metrics
from Graph import create_graphml
from Plot.Plotting_Group_Analysis import feature_table



def music_data(G, num_notes_normalized = None, num_notes = None, time_length = None, total_ticks = None, max_num_nodes = None):
    """ From a network obtains a list of features to be compared to other songs """
    feature_list = [] # average degree, average betweenness, average closeness, average clustering coef
    feature_name_list = ["Song"] # Name of features for the table plots (plus "Song")
    features_to_normalize = [] # Names of features to normalize (min/max) i.e., the according to the whole set of graphs/songs

    # Normalizing all values except clustering that by default is already "normalized"

    # # Average In-degree Unweighted
    # feature_list.append(Graph_metrics.average_indegree(G, normalize = True, weighted = False))
    # feature_name_list.append("Avg. In-degree")

    # Average In-degree Weighted
    feature_list.append(Graph_metrics.average_indegree(G, normalize = False, weighted = True)) # Normalizing bellow min/max corresponding to the whole dataset
    feature_name = "Avg. W.\nIn-Degree"
    feature_name_list.append(feature_name)
    features_to_normalize.append(feature_name)

    # # Average Betweenness Centrality
    # feature_list.append(Graph_metrics.average_betweenness(G, normalize = True))
    # feature_name_list.append("Avg. Betweenness Coef.")

    # Average Betweenness Centrality Weighted
    feature_list.append(Graph_metrics.average_betweenness(G, normalize = False, weighted =  True))
    feature_name = "Avg. W.\nBetweenness Cent."
    feature_name_list.append(feature_name)
    features_to_normalize.append(feature_name)

    # # Average Closeness Centrality (Normalized by default)
    # feature_list.append(Graph_metrics.average_closeness(G))
    # feature_name_list.append("Avg. Closeness Coef.")

    # Average Closeness Centrality (Normalized by default) Weighted
    feature_list.append(Graph_metrics.average_closeness(G, weighted = True))
    feature_name = "Avg. W.\nCloseness Cent."
    feature_name_list.append(feature_name)
    features_to_normalize.append(feature_name)

    # Number of Nodes normalized by the maximum number of nodes of the graphs being analysed
    # feature_list.append(G.number_of_nodes() / max_num_nodes)
    # feature_name_list.append("# Nodes")



    # Average Clustering Coefficient
    feature_list.append(Graph_metrics.average_clustering(G)) # Doesn't use weight and is normalized by default
    feature_name_list.append("Avg. Clustering\nCoef.")

    # Average Shortest Path Length (Normalized) Weighted
    feature_list.append(nx.average_shortest_path_length(G, weight = "weight")) # Normalizing bellow min/max corresponding to the whole dataset
    feature_name = "Avg. Shortest\nW. Path Length"
    feature_name_list.append(feature_name)
    features_to_normalize.append(feature_name)

    feature_list.append(nx.density(G)) # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.density.html?highlight=density#networkx.classes.function.density
    feature_name_list.append("Density")

    modularity, num_communities = Graph_metrics.modularity_louvain(G)
    feature_list.append(modularity)
    feature_name_list.append("Modularity")
    # feature_list.append(num_communities)
    # feature_name_list.append("#Communities")


    # # Nodes and Edges relative to duration - Adding 0 if the value doesn't exist to ensure that the feature vector (feature_list) has the same dimension for all songs. Needed for comparison and clustering
    # if time_length != 0:
    #     # Nodes per duration
    #     if G.number_of_nodes() != 0:
    #         feature_list.append(G.number_of_nodes() / time_length)
    #     else:
    #         feature_list.append(0)

    #     # Edges per duration
    #     if G.number_of_edges():
    #         feature_list.append(G.number_of_edges() / time_length)
    #     else:
    #         feature_list.append(0)
    # else:
    #     feature_list.append(0)
    #     feature_list.append(0)
    # feature_name_list.append("Nodes per seconds")
    # feature_name_list.append("Edges per seconds")

    # # Notes per duration (ticks)
    # if num_notes != 0:
    #     feature_list.append(num_notes/total_ticks) # Length of music (number of notes in track)
    # else:
    #     feature_list.append(0)
    # feature_name_list.append("Note per ticks")

    # # Notes per duration (seconds)
    # if num_notes_normalized != 0:
    #     feature_list.append(num_notes_normalized) # Length of music (number of notes in track)
    # else:
    #     feature_list.append(0)
    # feature_name_list.append("Note per seconds")

    return feature_list, feature_name_list, features_to_normalize



def create_networks(files_directory, max_nodes = True):
    """
    From a directory with MIDI files
    Creates a list that has an entry per song
    Each of those entries being a list itself with a network and a few values associated with it
    for further processing
    """

    # Obtain a list of the file names of all MIDI files in the directory (SongArena by Default). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

    list_files.sort() # Sorts the list alphabetically

    if len(list_files) == 0:
        print("The folder is empty")
        exit()

    print("Running for the following files:")
    for mid in list_files:
        print(mid)

    # Create the Graphs
    networks = []

    max_num_nodes = 0 # The max number of nodes of a Graph within this set

    tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand

    print("\n-----\nChosen Tracks:\n")

    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        filename = MIDI_general.midi_filename(mid_file)
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)

        network, notes, notes_duration, total_ticks = Music_Mapping.graph_note_pairs_weighted(mid_file, ticks = True, track_index = track_index)

        create_graphml(network, filename, files_directory)

        networks.append([network, mid_file, filename, notes, notes_duration, total_ticks])

        max_num_nodes = max(max_num_nodes, network.number_of_nodes())

    if max_nodes:
        return networks, max_num_nodes
    else:
        return networks




def feature_analysis(files_directory, normalized = True):
    """ Displaying a set of features for a dataset """
    networks = create_networks(files_directory, max_nodes = False)

    networks_feature_list = []
    filenames_list = []
    # for network in networks:
    for network, mid_file, filename, notes, notes_duration, total_ticks in networks:
        features, feature_names, features_to_normalize = music_data(network)
        networks_feature_list.append(features)
        filenames_list.append(filename)

    if normalized:
        networks_features = normalize_min_max(networks_feature_list, feature_names, features_to_normalize)
    else:
        networks_features = networks_feature_list

    feature_table(networks_features, feature_names, filenames_list, files_directory, model = None, normalized = normalized)

    return



def normalize_min_max(feature_list, feature_names, features_to_normalize):
    """ Normalizes features given the min and max of its values on a dataset """
    
    # Setting which features will be normalized given the names on the list features_to_normalize
    feature_indices_to_norm = []
    for i, feature in enumerate(feature_names[1:]):
        if feature in features_to_normalize:
            feature_indices_to_norm.append(i)


    for feature_index in feature_indices_to_norm: # Per Feature to be normalized
        # Finding the min and max values
        min_feature_value = feature_list[0][feature_index]
        max_feature_value = feature_list[0][feature_index]
        for i in range(1, len(feature_list)): # Per Song
            song_feature_value = feature_list[i][feature_index]
            min_feature_value = min(min_feature_value, song_feature_value)
            max_feature_value = max(max_feature_value, song_feature_value)
        
        # Normalizing
        for i in range(len(feature_list)): # Per Song
            feature_list[i][feature_index] -= min_feature_value
            feature_list[i][feature_index] /= (max_feature_value - min_feature_value)

    return feature_list



if __name__ == "__main__":
    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena")
        files_directory = config.ROOT + "\\SongArena" # Where the MIDI files to be analyzed are

    elif len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

    else:
        print("Too many arguments")
        exit()

    feature_analysis(files_directory)
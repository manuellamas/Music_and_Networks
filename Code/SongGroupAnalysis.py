""" Analyze several songs by resorting to Data Science tools, K-means,... """

import sys
import config
import os.path
from os import listdir

import mido
import networkx as nx

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np

import Music_Mapping
import MIDI_general
import Graph_metrics
import Plot.Plotting_Group_Analysis as plt_analysis
import TimeWindow
import MIDITimeSeries

def music_data(G, num_notes_normalized, time_length):
    """ From a network obtains a list of features to be compared to other songs """
    feature_list = [] # average degree, average betweenness, average closeness, average clustering coef

    # Normalizing all values except clustering that by default is already "normalized"
    feature_list.append(Graph_metrics.average_indegree(G)/(G.number_of_nodes() - 1))
    feature_list.append(Graph_metrics.average_betweenness(G, normalize = True))
    feature_list.append(Graph_metrics.average_closeness(G, normalize = True))
    feature_list.append(Graph_metrics.average_clustering(G))
    feature_list.append(nx.average_shortest_path_length(G))
    feature_list.append(nx.density(G))
    feature_list.append(Graph_metrics.modularity_louvain(G))

    # For new features -> Don't forget to add the features names to feature_names and feature_time_names

    # Notes and Edges relative to duration - Adding 0 if the value doesn't exist to ensure that the feature vector (feature_list) has the same dimension for all songs. Needed for comparison and clustering
    if time_length != 0:
        if G.number_of_nodes() != 0:
            feature_list.append(G.number_of_nodes() / time_length)
        else:
            feature_list.append(0)

        if G.number_of_edges():
            feature_list.append(G.number_of_edges() / time_length)
        else:
            feature_list.append(0)
    else:
        feature_list.append(0)
        feature_list.append(0)

    if num_notes_normalized != 0:
        feature_list.append(num_notes_normalized) # Length of music (number of notes in track)
    else:
        feature_list.append(0)

    return feature_list



def kmeans_analysis(networks_features):
    """ Apply kmeans to the vector of features obtained from the network of the song """
    num_clusters = np.arange(2, min(5, len(networks_features)))
    results = {}
    for size in num_clusters:
        kmeans = KMeans(n_clusters = size).fit(networks_features)
        predictions = kmeans.predict(networks_features)
        results[size] = silhouette_score(networks_features, predictions)

    ideal_size = max(results, key=results.get) # Ideal number of clusters

    # Right now I'm just repeating the algorithm with the ideal_size but it might be better to save all predictions (i.e., for each size) and then just use keep the one for the ideal_size
    kmeans = KMeans(n_clusters = ideal_size).fit(networks_features)
    predictions = kmeans.predict(networks_features)
    results[ideal_size] = silhouette_score(networks_features, predictions)

    return predictions



def dbscan_analysis(network_features):
    """ Apply DBSCAN to the vector of features obtained from the network of the song """
    db = DBSCAN(eps = 4.5, min_samples = 3).fit(network_features)
    db_clusters = db.labels_

    return db_clusters










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
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        network, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file)
        filename = MIDI_general.midi_filename(mid_file)

        nx.write_graphml(network, config.ROOT + "\\graphml_files\\" + filename + "_Graph.graphml") # Exporting graph to a graphml file
        network = nx.relabel_nodes(network, MIDI_general.note_mapping_dict(network)) # Adding labels according to the notes

        networks.append([network, mid_file, filename, notes])



    ##################
    # Usual Features #
    ##################

    # Feature List
    networks_feature_list = [] # Each entry is relative to a song

    networks_feature_time_list = [] # Features from TimeWindow
    filenames = []
    for network, mid_file, filename, notes in networks:
        filenames.append(filename) # Listing filenames for the feature table

        # Obtaining Time Length (if possible)
        time_length = 0
        try:
            time_length = mid_file.length
        except:
            print("This MIDI file is of type 2 (asynchronous) and so the length can't be computed")
            print("This song '" + filename + "'should probably be removed, or the analysis done without the length")

        if time_length == 0:
            networks_feature_list.append(music_data(network, 0, time_length))
        else:
            networks_feature_list.append(music_data(network, len(notes)/time_length, time_length))
                
        # Features from Time Window
        networks_feature_time_list.append(TimeWindow.time_window_features(mid_file))

    # feature_names = ["Song", "Avg. Degree", "Avg. Betweenness Coef.", "Avg. Closeness Coef.", "Avg. Clustering Coef.", "Avg. Shortest Path", "Density", "Nodes per duration", "Edges per duration", "Note 'density'"] # Note density refers to # Notes / Time Length
    feature_names = ["Song", "Avg. Degree", "Avg. Betweenness Coef.", "Avg. Closeness Coef.", "Avg. Clustering Coef.", "Avg. Shortest Path", "Density", "Modularity", "Nodes per duration", "Edges per duration", "Note 'density'"] # Note density refers to # Notes / Time Length
    feature_time_names = ["Song", "Avg. Degree (avg overtime)", "Avg. Degree (var overtime)", "Avg. Between (avg overtime)", "Avg. Between (var overtime)", "Avg. Closeness (avg overtime)", "Avg. Closeness (var overtime)", "Avg. ClusterCoeff (avg overtime)", "Avg. ClusterCoeff (var overtime)", "Density"] # Time Window Features


    # Feature Table
    plt_analysis.feature_table(networks_feature_list, feature_names, filenames, group_name)
    plt_analysis.feature_table(networks_feature_time_list, feature_time_names, filenames, group_name, type = "time")



    ##############
    # Clustering #
    ##############

    for i in range(len(networks_feature_list)):
        networks_feature_list[i] += networks_feature_time_list[i] # Adding these features for the clustering

    # k-means
    kmean_predictions = kmeans_analysis(networks_feature_list)
    plt_analysis.clustering_table(networks, kmean_predictions, "k-means", group_name)

    kmean_predictions = kmeans_analysis(networks_feature_time_list)
    plt_analysis.clustering_table(networks, kmean_predictions, "k-means", group_name, time = True)

    # DBSCAN
    dbscan_predictions = dbscan_analysis(networks_feature_list)
    plt_analysis.clustering_table(networks, dbscan_predictions,"DBSCAN", group_name)

    dbscan_predictions = dbscan_analysis(networks_feature_time_list)
    plt_analysis.clustering_table(networks, dbscan_predictions,"DBSCAN", group_name, time = True)



    print("\n\n----- %s seconds -----" % (time.time() - start_time))
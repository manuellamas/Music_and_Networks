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

def music_data(G):
    """ From a network obtains a list of features to be compared to other songs """
    feature_list = [] # average degree, average betweenness, average closeness, average clustering coef

    # Normalizing all values except clustering that by default is already "normalized"
    feature_list.append(Graph_metrics.average_degree(G)/(G.number_of_nodes() - 1))
    feature_list.append(Graph_metrics.average_betweenness(G, normalize = True))
    feature_list.append(Graph_metrics.average_closeness(G, normalize = True))
    feature_list.append(Graph_metrics.average_clustering(G))

    return feature_list



def kmeans_analysis(networks_features):
    """ Apply kmeans to the vector of features obtained from the network of the song """
    num_clusters = np.arange(2,5)
    results = {}
    for size in num_clusters:
        kmeans = KMeans(n_clusters = size).fit(networks_features)
        predictions = kmeans.predict(networks_features)
        results[size] = silhouette_score(networks_features, predictions)

    ideal_size = max(results, key=results.get)
    print(ideal_size)

    # Right now I'm just repeating the algorithm with the ideal_size but it might be better to save all predictions (i.e., for each size) and then just use keep the one for the ideal_size
    kmeans = KMeans(n_clusters = ideal_size).fit(networks_feature_list)
    predictions = kmeans.predict(networks_feature_list)
    results[ideal_size] = silhouette_score(networks_feature_list, predictions)
    print(predictions)

    return predictions



def dbscan_analysis(network_features):
    """ Apply DBSCAN to the vector of features obtained from the network of the song """
    DBSCAN(eps = 1, min_samples = 3).fit(networks)


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


    # Obtain a list of the file names of all MIDI files in the directory (SongArena). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

    # Create the Graphs
    networks = []
    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        network, notes = Music_Mapping.graph_note_pairs_weighted(mid_file)
        filename = MIDI_general.midi_filename(mid_file)

        networks.append([network, mid_file, filename, notes])


    # Feature List
    networks_feature_list = []
    for network, mid_file, filename, notes in networks:
        networks_feature_list.append(music_data(network))

    # Kmeans
    kmean_predictions = kmeans_analysis(networks_feature_list)
    plt_analysis.kmeans_clustering_table(networks, kmean_predictions)

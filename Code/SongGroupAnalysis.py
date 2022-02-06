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

def music_data(G, num_notes_normalized):
    """ From a network obtains a list of features to be compared to other songs """
    feature_list = [] # average degree, average betweenness, average closeness, average clustering coef

    # Normalizing all values except clustering that by default is already "normalized"
    feature_list.append(Graph_metrics.average_degree(G)/(G.number_of_nodes() - 1))
    feature_list.append(Graph_metrics.average_betweenness(G, normalize = True))
    feature_list.append(Graph_metrics.average_closeness(G, normalize = True))
    feature_list.append(Graph_metrics.average_clustering(G))

    if num_notes_normalized != 0:
        feature_list.append(num_notes_normalized) # Length of music (number of notes in track)

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
    kmeans = KMeans(n_clusters = ideal_size).fit(networks_features)
    predictions = kmeans.predict(networks_features)
    results[ideal_size] = silhouette_score(networks_features, predictions)
    print(predictions)

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

    elif len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

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
            networks_feature_list.append(music_data(network, 0))
        else:
            networks_feature_list.append(music_data(network, len(notes)/time_length))

    # k-means
    kmean_predictions = kmeans_analysis(networks_feature_list)
    plt_analysis.clustering_table(networks, kmean_predictions, "k-means")

    # DBSCAN
    dbscan_predictions = dbscan_analysis(networks_feature_list)
    print(len(dbscan_predictions))
    plt_analysis.clustering_table(networks, dbscan_predictions, "DBSCAN")

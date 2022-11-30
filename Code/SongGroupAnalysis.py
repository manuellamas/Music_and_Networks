""" Analyze several songs by resorting to k-means """

import sys
import config

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np

import MIDI_general
import Plot.Plotting_Group_Analysis as plt_analysis
import TimeWindow

from Feature_Analysis import normalize_min_max, music_data, create_networks



def kmeans_analysis(networks_features):
    """ Apply kmeans to the vector of features obtained from the network of the song """
    num_clusters = np.arange(2, min(6, len(networks_features) + 1)) # The 5 is to limit
    results = {}
    for size in num_clusters:
        kmeans = KMeans(n_clusters = size).fit(networks_features) # The algorithm used by default is Lloyd's https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
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






def main_analysis(files_directory):
    """
    The idea is for this to be ran at Full_Group_Analysis
    and so I should have only one place where I change things
    """


    networks = create_networks(files_directory, max_nodes = False)
    # networks, max_num_nodes = create_networks(files_directory)



    ##################
    # Usual Features #
    ##################

    # Feature List
    networks_feature_list = [] # Each entry is relative to a song
    networks_feature_time_list = [] # Features from TimeWindow

    tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand

    filenames = []
    for network, mid_file, filename, notes, notes_duration, total_ticks in networks:
        filenames.append(filename) # Listing filenames for the feature table

        # # Obtaining Time Length in seconds (if possible)
        # time_length_seconds = 0
        # note_density = 0
        # try:
        #     time_length_seconds = mid_file.length
        #     note_density = len(notes)/time_length_seconds
        # except:
        #     print("This MIDI file is of type 2 (asynchronous) and so the length can't be computed")
        #     print("This song '" + filename + "'should probably be removed, or the analysis done without the length")

        # features, feature_names, features_to_normalize = music_data(network, note_density, len(notes), time_length_seconds, total_ticks, max_num_nodes) # Currently getting feature_names repeatedly but only need it a single time
        features, feature_names, features_to_normalize = music_data(network) # Currently getting feature_names repeatedly but only need it a single time
        networks_feature_list.append(features)



        # Features from Time Window
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)
        networks_feature_time_list.append(TimeWindow.time_window_features(mid_file, track_index = track_index))



    # Normalizing Features Min-Max
    networks_feature_list = normalize_min_max(networks_feature_list, feature_names, features_to_normalize)






    # Features Names - Time Window
    feature_time_names = ["Song", "Avg. Degree (avg overtime)", "Avg. Degree (var overtime)", "Avg. Between (avg overtime)", "Avg. Between (var overtime)", "Avg. Closeness (avg overtime)", "Avg. Closeness (var overtime)", "Avg. ClusterCoeff (avg overtime)", "Avg. ClusterCoeff (var overtime)", "Density"] # Time Window Features


    ##############
    # Clustering #
    ##############


    # Adding the features obtained through Time Window on the "Main" set of features
    # for i in range(len(networks_feature_list)):
    #     networks_feature_list[i] += networks_feature_time_list[i] # Adding these features for the clustering

    
    ## k-means
    kmean_predictions = kmeans_analysis(networks_feature_list)
    ## plt_analysis.clustering_table(networks, kmean_predictions, "k-means", group_name) # Currently being outputted together with the feature table
    plt_analysis.cluster_feature_table(networks, kmean_predictions, "k-means", networks_feature_list, feature_names, files_directory = files_directory)


    # Time Window
    kmean_predictions = kmeans_analysis(networks_feature_time_list)
    plt_analysis.clustering_table(networks, kmean_predictions, "time_k-means", files_directory)
    # -----


    ## DBSCAN
    # dbscan_predictions = dbscan_analysis(networks_feature_list)
    # plt_analysis.clustering_table(networks, dbscan_predictions,"DBSCAN", group_name)

    # Time Window
    # dbscan_predictions = dbscan_analysis(networks_feature_time_list)
    # plt_analysis.clustering_table(networks, dbscan_predictions,"time_DBSCAN", group_name)
    # -----

    return










if __name__ == "__main__":

    import time
    start_time = time.time()

    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena")
        files_directory = config.ROOT + "\\SongArena" # Where the MIDI files to be analyzed are
        # group_name = "SongArena"

    elif len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are
        # group_name = sys.argv[-1].rsplit('\\', 1)[-1] # Used to denote the folder

    else:
        print("Too many arguments")
        exit()



    main_analysis(files_directory)

    print("\n\n----- %s seconds -----" % (time.time() - start_time))





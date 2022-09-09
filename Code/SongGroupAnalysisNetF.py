""" Analyze several songs by obtaining its NetF features """

import sys
import config

import Plot.Plotting_Group_Analysis as plt_analysis
import MIDITimeSeries

from SongGroupAnalysis import *



def main_analysis_netf(files_directory):


    networks = create_networks(files_directory, max_nodes = False)



    #################
    # NetF Features #
    #################

    netf_feature_list = [] # Each entry is relative to a song

    # Running the Rscript only once
    filenames = []
    networks_midi_files = []
    for i in range(len(networks)): # For each song/network
        networks_midi_files.append(networks[i][1]) # Storing the mid_files (objects)
        filenames.append(networks[i][2]) # Saving the filenames
    netf_all_series_strings = MIDITimeSeries.features_from_MIDI_series_group(networks_midi_files, num_quantiles = 8)


    for i in range(len(networks)):
        netf_strings = netf_all_series_strings[i] # Getting the net features for midi file i
        netf_float = []
        for i in range(len(netf_strings)):
            netf_float.append(float(netf_strings[i])) # Converting to float and appending all to a single list
        netf_feature_list.append(netf_float) # Each entry is a list with the netf features of a midi file



    # NetF Feature Table
    netf_feature_names = ["Song", "NVG - k", "NVG - d", "NVG - S", "NVG - C", "NVG - Q", "HVG - k" , "HVG - d", "HVG - S", "HVG - C", "HVG - Q", "QG - k", "QG - d", "QG - S", "QG - C", "QG - Q"]




    ###################
    # NetF Clustering #
    ###################

    ## k-means
    kmean_predictions = kmeans_analysis(netf_feature_list)
    # plt_analysis.clustering_table(networks, kmean_predictions, "netf_k-means", group_name) # Just the clustering without the features values
    plt_analysis.cluster_feature_table(networks, kmean_predictions, "netf_k-means", netf_feature_list, netf_feature_names, filenames, files_directory = files_directory)
    # -----




    ## DBSCAN
    # dbscan_predictions = dbscan_analysis(netf_feature_list)
    # plt_analysis.cluster_feature_table(networks, kmean_predictions, "netf_DBSCAN", netf_feature_list, netf_feature_names, filenames, files_directory = files_directory)
    # -----

    return






if __name__ == "__main__":

    import time
    start_time = time.time()

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



    main_analysis_netf(files_directory)

    print("\n\n----- %s seconds -----" % (time.time() - start_time))


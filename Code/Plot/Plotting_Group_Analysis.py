import matplotlib.pyplot as plt
import numpy as np

import config

def clustering_table(networks, cluster_predictions, model, group_name = "", labels = None):
    """ Plots a table with the songs/networks and its cluster resulting of the specified model """

    cluster_list = []
    if labels is None:
        for i in range(len(networks)):
            cluster_list.append([networks[i][2], cluster_predictions[i]]) # filename

    else:
        num_clusters = len(np.unique(cluster_predictions))
        list_artists = np.unique(labels)
        num_artists = len(list_artists)
        cluster_artist_count = [[0 for x in range(num_artists)] for x in range(num_clusters)] # Each entry will be a list corresponding to each cluster
        # And in that list will be the count for each artist [artist_a_count, artist_b_count,...]

        # Creating dictionary
        dict_artists = {}
        for i in range(num_artists):
            dict_artists[list_artists[i]] = i # From artist to num

        for i in range(len(networks)):
            cluster_list.append([networks[i][2], cluster_predictions[i], labels[i]]) # filename, labels

            if cluster_predictions[i] != -1: # Not noise points in DBSCAN
                cluster_artist_count[cluster_predictions[i]][dict_artists[labels[i]]] += 1

        cluster_artist = []
        for a in range(num_artists):
            max_value = 0
            max_cluster = -1
            for c in range(num_clusters):
                cluster_artist_count[c][a]
                max_value = max(max_value, cluster_artist_count[c][a])
                if max_value == cluster_artist_count[c][a]:
                    max_cluster = c
            
            cluster_artist.append(max_cluster) # Storing the number of the cluster that corresponds to the artist


    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes

    color_list = ["#ffffb3", "#ff803e", "#ffff68", "#ffa6bd", "#ffc100", "#ffcea2", "#ff8170"]
    # color_list = ["#ffffb300", "#ff803e75", "#ffff6800", "#ffa6bdd7", "#ffc10020", "#ffcea262", "#ff817066"]
    color_right = "green"
    color_wrong = "red"

    colors = []
    for i in range(len(cluster_predictions)):
        chosen_color = color_list[cluster_predictions[i]]
        if labels is None:
            colors.append([chosen_color, chosen_color])
        else:
            artist_cluster = cluster_artist[dict_artists[labels[i]]] # The cluster corresponding to the artist of the i song

            if artist_cluster == cluster_predictions[i]:
                cluster_color = color_right
            else:
                cluster_color = color_wrong
            colors.append([chosen_color, chosen_color, cluster_color])

    if labels is None:
        columns = ["Song", "Cluster"]
    else:
        columns = ["Song", "Cluster", "Artist/Band"]

    rows = [] #, rowLabels = rows
    tab = ax.table(cellText = cluster_list, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)

    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below
    tab.set_fontsize(8)
    tab.auto_set_column_width(col=list(range(len(columns)))) # Sets Column width automatically

    fig.tight_layout()

    plt.savefig(config.ROOT + "\\Plots\\SongGroupAnalysis\\" + group_name + "_" + model + "_clustering.png")
    print("Plot at", model + "_clustering" + ".png")



def feature_table(network_features, feature_names, file_names, group_name = ""):
    """ Plots a table with all features being analyzed """


    network_feature_list = [[] for i in range(len(network_features))]

    for i in range(len(network_features)): # Going through every song
        # File Name
        network_feature_list[i].append(file_names[i])

        # Features
        network_feature_list[i] += network_features[i] # Adding the features to the list
        
        if len(network_feature_list[i]) != len(feature_names): # For the networks that don't have the length feature for some reason
            network_feature_list[i].append(0)

        for j in range(1, len(network_feature_list[i])): # Rounding Values
            network_feature_list[i][j] = "{:.3f}".format(network_feature_list[i][j])


        



    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes


    columns = feature_names


    print(list(range(len(network_feature_list)+1)))

    # rows = [] #, rowLabels = rows
    tab = ax.table(cellText = network_feature_list, colLabels = columns, loc = "center", cellLoc = "center")
    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below

    tab.set_fontsize(8)
    tab.auto_set_column_width(col = list(range(len(columns)))) # Sets Column width automatically

    cells = tab.properties()["celld"]

    # Overriding the cellLoc = "center"
    for j in range(1, len(columns)):
        for i in range(1, len(network_feature_list) + 1): # For each row. +1 because the column headers cells are included
            cells[i, j].set_text_props(ha = "right") # Centering column j



    fig.tight_layout()

    plt.savefig(config.ROOT + "\\Plots\\SongGroupAnalysis\\" + group_name+ "_features.png", bbox_inches='tight')
    print("Plot at", "features" + ".png")

    return
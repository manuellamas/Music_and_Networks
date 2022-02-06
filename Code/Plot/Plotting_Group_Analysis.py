import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import config

import Graph_metrics

def clustering_table(networks, cluster_predictions, model, labels = None):
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

    plt.savefig(config.ROOT + "\\Plots\\SongGroupAnalysis\\"+ model +"_clustering.png")




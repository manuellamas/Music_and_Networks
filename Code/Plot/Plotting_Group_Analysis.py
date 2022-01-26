import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import config

import Graph_metrics

def kmeans_clustering_table(networks, cluster_predictions):
    """ Plots a table with the songs/networks by resulting k-means cluster """

    cluster_list = []
    for i in range(len(networks)):
        cluster_list.append([networks[i][2], cluster_predictions[i]]) # filename

    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes

    color_list = ["b","r","g","y","p"]
    colors = []
    for i in range(len(cluster_predictions)):
        chosen_color = color_list[cluster_predictions[i]]
        colors.append([chosen_color, chosen_color])

    columns = ["Song", "Cluster"]
    rows = [] #, rowLabels = rows
    ax.table(cellText = cluster_list, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)
    fig.tight_layout()

    plt.savefig(config.ROOT + "\\Plots\\Single\\k-means_clustering.png")



    # Network | Cluster number
    # color row by cluster number, specify a list of hexcolors beforehand
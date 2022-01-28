import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import config

import Graph_metrics

def clustering_table(networks, cluster_predictions, model):
    """ Plots a table with the songs/networks and its cluster resulting of the specified model """

    cluster_list = []
    for i in range(len(networks)):
        cluster_list.append([networks[i][2], cluster_predictions[i]]) # filename

    fig, ax = plt.subplots()
    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes

    # color_list = ["b","r","g","y","greenyellow"]
    color_list = ["#ffffb3", "#ff803e", "#ffff68", "#ffa6bd", "#ffc100", "#ffcea2", "#ff8170"]
    # color_list = ["#ffffb300", "#ff803e75", "#ffff6800", "#ffa6bdd7", "#ffc10020", "#ffcea262", "#ff817066"]
    colors = []
    for i in range(len(cluster_predictions)):
        chosen_color = color_list[cluster_predictions[i]]
        colors.append([chosen_color, chosen_color])

    columns = ["Song", "Cluster"]
    rows = [] #, rowLabels = rows
    ax.table(cellText = cluster_list, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)
    fig.tight_layout()

    plt.savefig(config.ROOT + "\\Plots\\Single\\"+ model +"_clustering.png")




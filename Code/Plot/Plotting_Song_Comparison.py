import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import config

import Graph_metrics

# Degree Distribution
def degree_distribution_comparison_plot(networks, line = True, scale = "linear", plot_folder = None):
    """ Creates a plot of a network's degree distribution linear (or loglog if specified) """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network


        degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
        degree_sequence = np.array(degree_sequence_list)

        labels, counts = np.unique(degree_sequence, return_counts=True)
        num_nodes = G.number_of_nodes()
        relative_counts = [c/num_nodes for c in counts]
        plt.scatter(labels, relative_counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, relative_counts)


    # Design
    if scale == "linear":
        title = "Degree Distribution"
    elif scale == "loglog":
        title = "Degree Distribution" + " LogLog"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes/total')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    if scale == "loglog":
        # Setting LogLog Scale
        ax1.set_xscale("log", base=10)
        ax1.set_yscale("log", base=10)

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = "_" + plot_folder

    if scale == "loglog":
        plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\Degree_Distribution_LogLog" + group_name + ".png")
    else:
        plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\Degree_Distribution" + group_name + ".png")



# Betweenness Centrality
def betwenness_comparison_plot(networks, line = True, plot_folder = None):
    """ Creates a plot of the betweenness centrality distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        betwenness_values = Graph_metrics.list_betweenness_centrality(G)

        betweenness_sequence_list = sorted(betwenness_values, reverse = True)
        betwenness_sequence = np.array(betweenness_sequence_list)

        labels, counts = np.unique(betwenness_sequence, return_counts=True)
        num_nodes = G.number_of_nodes()
        relative_counts = [c/num_nodes for c in counts]
        plt.scatter(labels, relative_counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, relative_counts)


    # Design
    title = "Betweenness Centrality"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Betweenness')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = "_" + plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\Betweenness_Distribution" + group_name + ".png")



# Betweenness Centrality (Side-by-side)
def betwenness_comparison_plot_sides(networks, line = True, plot_folder = None):
    """ Creates a plot of the betweenness centrality distribution of a Graph """
    fig, axs = plt.subplots(len(networks))
    # fig.subplots_adjust(wspace=0.2)
    fig.subplots_adjust(hspace=0.5)

    ax_num = 0

    # Since I'm working with relative values
    min_y_value = 1
    max_y_value = 0

    for network in networks:
        G, midi_file, midi_title, notes = network
        ax = axs[ax_num]

        betwenness_values = Graph_metrics.list_betweenness_centrality(G)

        betweenness_sequence_list = sorted(betwenness_values, reverse = True)
        betwenness_sequence = np.array(betweenness_sequence_list)

        labels, counts = np.unique(betwenness_sequence, return_counts=True)
        num_nodes = G.number_of_nodes()
        relative_counts = [c/num_nodes for c in counts]
        ax.scatter(labels, relative_counts, s=10, label = midi_title.replace("_", " "))

        min_y_value = min(min_y_value,min(relative_counts))
        max_y_value = max(max_y_value,max(relative_counts))

        if line:
            # Create a line on top of a scatter plot
            ax.plot(labels, relative_counts)

        # Design
        # title = "Betweenness Centrality"
        # plt.title(title)

        # Axis Labels
        # ax.set_xlabel('Betweenness')
        ax.set_ylabel('#Nodes')

        # Axis Ticks
        # ax.yaxis.set_major_locator(ticker.LinearLocator(5))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers
        ax.locator_params(nbins=4, axis='y')


        # Legend
        ax.legend(loc="upper right")

        ax_num += 1

    for ax in axs:
        # ax.ylim([0,10]) # Forces the y axis to show only values on the speficied interval
        ax.set(ylim=(min_y_value, max_y_value))

    group_name = ""
    if plot_folder is not None:
        group_name = "_" + plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\Betweenness_Distribution_(side-by-side)" + group_name + ".png")



# Closeness Centrality
def closeness_comparison_plot(networks, line = True, plot_folder = None):
    """ Creates a plot of the closeness centrality distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        closeness_values = Graph_metrics.list_closeness_centrality(G)

        closeness_sequence_list = sorted(closeness_values, reverse = True)
        closeness_sequence = np.array(closeness_sequence_list)

        labels, counts = np.unique(closeness_sequence, return_counts=True)
        num_nodes = G.number_of_nodes()
        relative_counts = [c/num_nodes for c in counts]
        plt.scatter(labels, relative_counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, relative_counts)


    # Design
    title = "Closeness Centrality"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Closeness')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = "_" + plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\Closeness_Distribution" + group_name + ".png")



# Clustering Coefficient
def clustering_coef_comparison_plot(networks, line = True, plot_folder = None):
    """ Creates a plot of the clustering coefficient distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        clust_coef_values = Graph_metrics.list_clustering_coefficient(G)

        clust_coef_sequence_list = sorted(clust_coef_values, reverse = True)
        clust_coef_sequence = np.array(clust_coef_sequence_list)

        labels, counts = np.unique(clust_coef_sequence, return_counts=True)
        num_nodes = G.number_of_nodes()
        relative_counts = [c/num_nodes for c in counts]
        plt.scatter(labels, relative_counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, relative_counts)


    # Design
    title = "Clustering Coefficient"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Clustering Coefficient')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = "_" + plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\Clustering_Coefficient_Distribution" + group_name + ".png")



# Edges Ranking

# import pandas as pd
def edges_rank(network):
    """ Plots a table with the rank of the edges by weight """
    edges_list = [] # entries of the form [NodeA, NodeB, Weight] the edge being NodeA -> NodeB
    for edge in network.edges.data():
        edges_list.append([edge[0], edge[1], edge[2]["weight"]])
    edges_list.sort(key = lambda e: e[2], reverse = True)
    
    fig, ax = plt.subplots()

    # Hide axes
    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")

    # df = pd.DataFrame()

    plt.show()

    return


# import networkx as nx
# G1 = nx.DiGraph()
# G1.add_weighted_edges_from([(1,2,3),(1,5,1),(2,3,4)])
# edges_rank(G1)
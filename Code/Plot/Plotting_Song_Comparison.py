import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

from os import mkdir
import os.path
import config

import Graph_metrics
from Plotting import edges_rank_network

# Support Function
def check_dir(dir):
    """ Checks if directory exists, else it creates it """

    # Checking if path exists
    path_exists = os.path.exists(dir)

    if not path_exists:
        mkdir(dir)
        print("The following directory was created", dir)


#------------------------------------------------------------#
#----------------------------Main----------------------------#
#------------------------------------------------------------#

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
        relative_counts = [c/(num_nodes - 1) for c in counts] # Normalized
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

    # Exporting to PNG
    group_name = ""
    if plot_folder is not None:
        # group_name = "_" + plot_folder
        group_name = plot_folder

    if scale == "loglog":
        plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name + "\\Degree_Distribution_LogLog" + group_name + ".png")
    else:
        plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name + "\\Degree_Distribution" + group_name + ".png")



# Betweenness Centrality
def betwenness_comparison_plot(networks, line = True, plot_folder = None):
    """ Creates a plot of the betweenness centrality distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        betwenness_values = Graph_metrics.list_betweenness_centrality(G, normalize = True)

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
    ax1.set_ylabel('#Nodes/total')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Legend
    plt.legend(loc="upper right")

    # Exporting to PNG
    group_name = ""
    if plot_folder is not None:
        # group_name = "_" + plot_folder
        group_name = plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name + "\\Betweenness_Distribution" + group_name + ".png")



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

        betwenness_values = Graph_metrics.list_betweenness_centrality(G, normalize = True)

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
        ax.set_ylabel('#N/total')

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

    # Exporting to PNG
    group_name = ""
    if plot_folder is not None:
        # group_name = "_" + plot_folder
        group_name = plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name + "\\Betweenness_Distribution_(side-by-side)" + group_name + ".png")



# Closeness Centrality
def closeness_comparison_plot(networks, line = True, plot_folder = None):
    """ Creates a plot of the closeness centrality distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        closeness_values = Graph_metrics.list_closeness_centrality(G, normalize = True)

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
    ax1.set_ylabel('#Nodes/total')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Legend
    plt.legend(loc="upper right")

    # Exporting to PNG
    group_name = ""
    if plot_folder is not None:
        # group_name = "_" + plot_folder
        group_name = plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name + "\\Closeness_Distribution" + group_name + ".png")



# Clustering Coefficient
def clustering_coef_comparison_plot(networks, line = True, plot_folder = None):
    """ Creates a plot of the clustering coefficient distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        clust_coef_values = Graph_metrics.list_clustering_coefficient(G) # Already normalized since values belongs to [0,1]

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
    ax1.set_ylabel('#Nodes/total')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Legend
    plt.legend(loc="upper right")

    # Exporting to PNG
    group_name = ""
    if plot_folder is not None:
        # group_name = "_" + plot_folder
        group_name = plot_folder

    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + group_name + "\\Clustering_Coefficient_Distribution" + group_name + ".png")



# Edge Ranking Table (Comparison)
def edges_rank_comparison(networks, top = 20, plot_folder = None):
    """ Plots a table with the rank of the edges by weight - Comparing several songs """

    edges_list_all = [[] for x in range(top)]

    edges_list_sum = [[] for x in range(len(networks))]
    network_index = 0

    columns = []
    for network in networks:
        G, midi_file, filename, notes = network
        columns.append(filename)
        edges_list_formatted = edges_rank_network(G, "group", top)
        for i in range(len(edges_list_formatted)): # Not 'len(top)' since some songs may have fewer than (the number) top edges. The padding to fill those voids is made after it
            edges_list_all[i].append(edges_list_formatted[i][0]) # Adding a column going through every i row
            edges_list_sum[network_index].append(edges_list_formatted[i][1]) # Ordered in a different way from edges_list_all. Every entry is a list with all edges (cumulative sum) of each music, and not spread out on a column
        if len(edges_list_formatted) < top:
            for i in range(len(edges_list_formatted), top): # Adding the missing entries. The rows between the end of edges_list_formatted and top (the total number of rows)
                edges_list_all[i].append("")
                # No edges_list_sum because I only append the existing values
        network_index += 1

    fig, ax = plt.subplots()

    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes



    color_list = ["#ffffb3", "#ff803e", "#ffff68", "#ffa6bd", "#ffc100", "#ffcea2", "#ff8170"]
    # Maybe it would be better to use just one color that gets darker (or maybe less transparent)

    colors = [[] for i in range(top)]
    for i in range(len(networks)): # For each song, which is a column
        levels = [l/100 for l in range(0, 100 + 1, 20)]
        next_level = 1
        current_level = 0

        for j in range(len(edges_list_sum[i])): # For each edge, which is a row (that can be different for each song of course)
            new_level = False

            while next_level < len(levels) and edges_list_sum[i][j] > levels[next_level]: # First condition is there due to aproximation errors ending up above 1.0
                next_level += 1
                new_level = True

            chosen_color = color_list[current_level]
            colors[j].append(chosen_color)
            # colors[j][i].append(chosen_color)

            if new_level:
                # current_level += 1
                current_level = next_level - 1

        for j in range(len(edges_list_sum[i]), top): # Dealing with missing entries
            colors[j].append("white")
            pass

    rows = [] #, rowLabels = rows
    tab = ax.table(cellText = edges_list_all, colLabels = columns, loc = "center", cellLoc = "center", cellColours=colors)

    tab.auto_set_font_size(False) # Makes font size not automatic and instead choose a font size below
    tab.set_fontsize(8)
    tab.auto_set_column_width(col=list(range(len(columns)))) # Sets Column width automatically

    fig.tight_layout()


    # Exporting to PNG
    group_name = ""
    if plot_folder is not None:
        group_name = plot_folder + "_"
        plot_folder += "\\" 
    else:
        plot_folder = ""

    print("Plot at", plot_folder + group_name + "Edge_Rank" + ".png")
    plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder + group_name + "Edge_Rank" + ".png", bbox_inches='tight')
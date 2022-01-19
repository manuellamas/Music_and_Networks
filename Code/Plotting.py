from asyncio.windows_events import NULL
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import os.path

import Graph_metrics
import MIDI_general

########## Graph Analysis ##########
def degree_distribution_histogram(G, filename):
    degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
    degree_sequence = np.array(degree_sequence_list)

    labels, counts = np.unique(degree_sequence, return_counts=True)

    print("Degree sequence: ", degree_sequence)
    fig1, ax1 = plt.subplots()

    # Bar Plot
    plt.bar(labels, counts, width=1) # The width allows to erase the space between each bar
    # plt.gca().set_xticks(labels) # Sets the x-axis labels to show all values that the array has
    # Might be interesting to define number of ticks (equally spaced) regardless of the amplitude. So say show 5 x-axix labels on every graph for example

    # Design
    title = "Degree Distribution" + " " + filename
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes')

    # Legend
    # plt.legend(loc="upper left")

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    plt.savefig(parent_directory + "\\Plots\\Single\\Degree_Distribution_Histogram_" + filename + ".png")
    # plt.show()



def degree_distribution_scatter_plot(G, filename):
    degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
    degree_sequence = np.array(degree_sequence_list)

    labels, counts = np.unique(degree_sequence, return_counts=True)
    # Turn absolute values into relative ones
    num_nodes = G.number_of_nodes()
    relative_counts = [c/num_nodes for c in counts]

    fig1, ax1 = plt.subplots()

    # Design
    title = "Degree Distribution" + " " + filename
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    # ax1.set_ylabel('#Nodes')
    ax1.set_ylabel('Relative Frequency')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    plt.scatter(labels, relative_counts, s=10)
    plt.savefig(parent_directory + "\\Plots\\Single\\Degree_Distribution_" + filename + ".png")

########## Graph Analysis End ##########



########## Musics Comparison ##########
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

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = plot_folder

    if scale == "loglog":
        plt.savefig(parent_directory + "\\Plots\\SongComparisonOutputFiles\\Degree_Distribution_LogLog_" + group_name + ".png")
    else:
        plt.savefig(parent_directory + "\\Plots\\SongComparisonOutputFiles\\Degree_Distribution_" + group_name + ".png")



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
        plt.scatter(labels, counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, counts)


    # Design
    title = "Betweenness Centrality"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Betweenness')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = plot_folder

    plt.savefig(parent_directory + "\\Plots\\SongComparisonOutputFiles\\Betweenness_Distribution_" + group_name + ".png")



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
        plt.scatter(labels, counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, counts)


    # Design
    title = "Closeness Centrality"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Closeness')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = plot_folder

    plt.savefig(parent_directory + "\\Plots\\SongComparisonOutputFiles\\Closeness_Distribution_" + group_name + ".png")



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
        plt.scatter(labels, counts, s=10, label = midi_title.replace("_", " "))

        if line:
            # Create a line on top of a scatter plot
            plt.plot(labels, counts)


    # Design
    title = "Clustering Coefficient"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Clustering Coefficient')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    # Legend
    plt.legend(loc="upper right")

    group_name = ""
    if plot_folder is not None:
        group_name = plot_folder

    plt.savefig(parent_directory + "\\Plots\\SongComparisonOutputFiles\\Clustering_Coefficient_Distribution_" + group_name + ".png")


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

########## Musics Comparison End ##########



########## Time Window ##########
def average_degree_time_window(average_degrees, time_interval, time_skip, filename, program = None):
    x_axis = []
    time_window_center = time_interval/2 # The moment (tick) at the center of the current window
    for i in range(len(average_degrees)):
        x_axis.append(time_window_center) # The time window is centered on this time (tick)
        time_window_center += time_skip

    fig1, ax1 = plt.subplots()

    # Design
    if program is None:
        title = "Average Degree" + " - " + filename
    else:
        program_category, program_instrument = MIDI_general.midi_program_num_to_name(program, instrument = True)
        title = "Average Degree" + " - " + filename + " - " + program_category + ", " + program_instrument
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Center Tick') # The center time (tick) of the window being analyzed
    ax1.set_ylabel('Average Degree')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    plt.ylim([0,10]) # Forces the y axis to show only values on the speficied interval

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    plt.scatter(x_axis, average_degrees, s=10)
    plt.savefig(parent_directory + "\\Plots\\Time_Window\\Average_Distribution_" + filename + "_I-" + str(time_interval) + "_S-" + str(time_skip) + ".png")
    # plt.savefig(parent_directory + "\\Plots\\Time_Window\\Average_Distribution_" + filename + ".png")
    

    return
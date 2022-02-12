import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import config

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

    plt.savefig(config.ROOT + "\\Plots\\Single\\Degree_Distribution_Histogram_" + filename + ".png")
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

    plt.scatter(labels, relative_counts, s=10)
    plt.savefig(config.ROOT + "\\Plots\\Single\\Degree_Distribution_" + filename + ".png")



def edges_rank_network(network, plot_type, top = 20):
    """ Obtain a list of the edges (ranked by weight) formatted for a table plot """
    edges_list = [] # entries of the form [NodeA, NodeB, Weight] the edge being NodeA -> NodeB
    total_weight = 0

    for edge in network.edges.data():
        edges_list.append([edge[0], edge[1], edge[2]["weight"]])
        total_weight += edge[2]["weight"]
    edges_list.sort(key = lambda e: e[2], reverse = True)

    edges_list = edges_list[:top] # Sticking only with the top "top" edges (e.g. top 20 edges)
    edges_list_formatted = []
    if plot_type == "single": # Only lookint at one song
        for edge in edges_list:
            edge_origin = MIDI_general.midi_num_to_note(edge[0])
            edge_end = MIDI_general.midi_num_to_note(edge[1])
            edge_label = str(edge_origin) + " -> " + str(edge_end)
            edges_list_formatted.append([edge_label, edge[2]])

    elif plot_type == "group": # Looking at several songs at once
        sum = 0
        for edge in edges_list:
            edge_origin = MIDI_general.midi_num_to_note(edge[0])
            edge_end = MIDI_general.midi_num_to_note(edge[1])
            edge_label = str(edge_origin) + " -> " + str(edge_end)
            sum += edge[2]/total_weight # This is already the cumulative sum of the weights of the edges of this network (starting with the 'heaviest' edge)
            edges_list_formatted.append([edge_label, sum])

    return edges_list_formatted

def edges_rank(network, filename, top = 20):
    """ Plots a table with the rank of the edges by weight """

    edges_list_formatted = edges_rank_network(network, "single", top)

    fig, ax = plt.subplots()

    fig.patch.set_visible(False) # Removing 'background'
    ax.axis("off") # Hide axes

    columns = ["Edge", "Frequency (weight)"]
    rows = [] #, rowLabels = rows
    ax.table(cellText = edges_list_formatted, colLabels = columns, loc = "center", cellLoc = "center")
    fig.tight_layout()

    plt.savefig(config.ROOT + "\\Plots\\Single\\Edge_Rank_" + filename + ".png")

########## Graph Analysis End ##########







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

    plt.scatter(x_axis, average_degrees, s=10)
    plt.savefig(config.ROOT + "\\Plots\\Time_Window\\Average_Distribution_" + filename + "_I-" + str(time_interval) + "_S-" + str(time_skip) + ".png")
    # plt.savefig(config.ROOT + "\\Plots\\Time_Window\\Average_Distribution_" + filename + ".png")
    

    return
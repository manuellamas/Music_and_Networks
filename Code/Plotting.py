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
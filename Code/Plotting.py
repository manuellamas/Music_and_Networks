import matplotlib.pyplot as plt
import numpy as np
import os.path

def DegreeDistributionHistogram(G, file):
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
    title = "Degree Distribution" + " " + file
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes')

    # Legend
    # plt.legend(loc="upper left")

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    plt.savefig(parent_directory + "\\Plots\\Degree_Distribution_" + file + ".png")
    # plt.savefig("../Plots/Degree_Distribution_" + file + ".png")
    # plt.show()

# def DegreeDistributionScatterPlot(G):

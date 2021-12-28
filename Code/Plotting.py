import matplotlib.pyplot as plt
from matplotlib import ticker
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
    # plt.show()

def DegreeDistributionScatterPlot(G, file):
    degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
    degree_sequence = np.array(degree_sequence_list)

    labels, counts = np.unique(degree_sequence, return_counts=True)

    fig1, ax1 = plt.subplots()

    # Design
    title = "Degree Distribution" + " " + file
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    plt.scatter(labels, counts, s=10)
    plt.savefig(parent_directory + "\\Plots\\Degree_Distribution_ScatterPlot_" + file + ".png")


def DegreeDistributionComparison(networks):
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title = network


        degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
        degree_sequence = np.array(degree_sequence_list)

        labels, counts = np.unique(degree_sequence, return_counts=True)
        plt.scatter(labels, counts, s=10, label = midi_title.replace("_", " "))


    # Design
    title = "Degree Distribution"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    # Legend
    plt.legend(loc="upper right")

    plt.savefig(parent_directory + "\\SongArena\\SongComparisonOutputFiles\\Degree_Distribution_" + "Song_Arena" + ".png")


def DegreeDistributionComparisonLogLog(networks):
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title = network


        degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
        degree_sequence = np.array(degree_sequence_list)

        labels, counts = np.unique(degree_sequence, return_counts=True)
        plt.scatter(labels, counts, s=10, label = midi_title.replace("_", " "))


    # Design
    title = "Degree Distribution"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes')

    # Axis Ticks
    # ax1.yaxis.set_major_locator(ticker.LinearLocator(5))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # Sets the ticks to only be integers

    # Setting LogLog Scale
    ax1.set_xscale("log", base=10)
    ax1.set_yscale("log", base=10)

    # Getting the correct path for the Plot folder
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    # Legend
    plt.legend(loc="upper right")

    plt.savefig(parent_directory + "\\SongArena\\SongComparisonOutputFiles\\Degree_Distribution_LogLog_" + "Song_Arena" + ".png")
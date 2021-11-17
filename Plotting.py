import matplotlib.pyplot as plt
import numpy as np

def DegreeDistribution(G):
    degree_sequence_list = sorted([d for n, d in G.degree()], reverse = True)
    degree_sequence = np.array(degree_sequence_list)

    labels, counts = np.unique(degree_sequence, return_counts=True)

    print(degree_sequence)
    fig1, ax1 = plt.subplots()

    # Bar Plot
    plt.bar(labels, counts, width=1) # The width allows to erase the space between each bar
    plt.gca().set_xticks(labels) # Sets the x-axis labels to show all values that the array has

    # Design
    title = "Degree Distribution"
    plt.title(title)

    # Axis Labels
    ax1.set_xlabel('Degree')
    ax1.set_ylabel('#Nodes')

    # Legend
    # plt.legend(loc="upper left")

    plt.savefig("Plots/Degree_Distribution_Histogram.png")
    # plt.show()
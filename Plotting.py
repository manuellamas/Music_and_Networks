import matplotlib.pyplot as plt

def DegreeDistribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse = True)

    fig1, ax1 = plt.subplots()
    
    # plt.plot(k, degree_sequence)
    plt.hist(degree_sequence)

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
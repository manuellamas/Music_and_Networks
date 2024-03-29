import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

import config

import Graph_metrics
from Plotting import edges_rank_network


#------------------------------------------------------------#
#----------------------------Main----------------------------#
#------------------------------------------------------------#

# Degree Distribution
def degree_distribution_comparison_plot(networks, line = True, scale = "linear", plot_folder = None, files_directory = ""):
    """ Creates a plot of a network's degree distribution linear (or loglog if specified) """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network


        degree_sequence_list = sorted([d for n, d in G.degree(weight = "weight")], reverse = True)
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
    if files_directory == "":
        if plot_folder is not None:
            group_name = plot_folder + "_"
            plot_folder = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder
        else:
            plot_folder = ""
    else:
        plot_folder = files_directory + "\\SongGroupAnalysis\\Comparison"
        group_name = files_directory.rsplit("\\")[-1]

    if scale == "loglog":
        plt.savefig(plot_folder + "\\" + group_name + "_" + "Degree_Distribution_LogLog" + ".png")
        print("Plot at", plot_folder + "\\" + group_name + "_" + "Degree_Distribution_LogLog" + ".png")
    else:
        plt.savefig(plot_folder + "\\" + group_name + "_" + "Degree_Distribution" + ".png")
        print("Plot at", plot_folder + "\\" + group_name + "_" + "Degree_Distribution" + ".png")
    
    plt.close()

# Betweenness Centrality
def betwenness_comparison_plot(networks, line = True, plot_folder = None, files_directory = ""):
    """ Creates a plot of the betweenness centrality distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        betwenness_values = Graph_metrics.list_betweenness_centrality(G, normalize = True, weighted = True)

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
    if files_directory == "":
        if plot_folder is not None:
            group_name = plot_folder + "_"
            plot_folder = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder
        else:
            plot_folder = ""
    else:
        plot_folder = files_directory + "\\SongGroupAnalysis\\Comparison"
        group_name = files_directory.rsplit("\\")[-1]

    plt.savefig(plot_folder + "\\" + group_name + "_" + "Betweenness_Distribution" + ".png")
    plt.close()
    print("Plot at", plot_folder + "\\" + group_name + "_" + "Betweenness_Distribution" + ".png")


# Betweenness Centrality (Side-by-side)
def betwenness_comparison_plot_sides(networks, line = True, plot_folder = None, files_directory = ""):
    """ Creates a plot of the betweenness centrality distribution of a Graph """
    fig, axs = plt.subplots(len(networks))
    # fig.subplots_adjust(wspace=0.2)

    fig.set_size_inches(7, 6, forward=True)
    fig.subplots_adjust(hspace=1)

    ax_num = 0

    # Since I'm working with relative values
    min_y_value = 1
    max_y_value = 0

    for network in networks:
        G, midi_file, midi_title, notes = network
        ax = axs[ax_num]

        betwenness_values = Graph_metrics.list_betweenness_centrality(G, normalize = True, weighted = True)

        betweenness_sequence_list = sorted(betwenness_values, reverse = True)
        betwenness_sequence = np.array(betweenness_sequence_list)

        labels, counts = np.unique(betwenness_sequence, return_counts=True)
        num_nodes = G.number_of_nodes()
        relative_counts = [c/num_nodes for c in counts]
        ax.scatter(labels, relative_counts, s=10, label = midi_title.replace("_", " ").replace(" - ", "\n"))

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
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), prop={'size': 8}) # Places center left of the legend at the designated position (in axes coordinates)

        ax_num += 1

    for ax in axs:
        # ax.ylim([0,10]) # Forces the y axis to show only values on the speficied interval
        ax.set(ylim=(min_y_value, max_y_value))

    # Exporting to PNG
    if files_directory == "":
        if plot_folder is not None:
            group_name = plot_folder + "_"
            plot_folder = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder
        else:
            plot_folder = ""
    else:
        plot_folder = files_directory + "\\SongGroupAnalysis\\Comparison"
        group_name = files_directory.rsplit("\\")[-1]

    # plt.savefig(config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder + group_name + "_" + "Betweenness_Distribution_(side-by-side)" + ".png")
    plt.savefig(plot_folder + "\\" + group_name + "_" + "Betweenness_Distribution_(side-by-side)" + ".png", bbox_inches = "tight") # bbox_inches tries to fit the legends on the figure
    plt.close()
    print("Plot at", plot_folder + "\\" + group_name + "_" + "Betweenness_Distribution_(side-by-side)" + ".png")


# Closeness Centrality
def closeness_comparison_plot(networks, line = True, plot_folder = None, files_directory = ""):
    """ Creates a plot of the closeness centrality distribution of a Graph """
    fig1, ax1 = plt.subplots()

    for network in networks:
        G, midi_file, midi_title, notes = network

        closeness_values = Graph_metrics.list_closeness_centrality(G, weighted = True)

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
    if files_directory == "":
        if plot_folder is not None:
            group_name = plot_folder + "_"
            plot_folder = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder
        else:
            plot_folder = ""
    else:
        plot_folder = files_directory + "\\SongGroupAnalysis\\Comparison"
        group_name = files_directory.rsplit("\\")[-1]

    plt.savefig(plot_folder + "\\" + group_name + "_" + "Closeness_Distribution" + ".png")
    plt.close()
    print("Plot at", plot_folder + "\\" + group_name + "_" + "Closeness_Distribution" + ".png")


# Clustering Coefficient
def clustering_coef_comparison_plot(networks, line = True, plot_folder = None, files_directory = ""):
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
    if files_directory == "":
        if plot_folder is not None:
            group_name = plot_folder + "_"
            plot_folder = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder
        else:
            plot_folder = ""
    else:
        plot_folder = files_directory + "\\SongGroupAnalysis\\Comparison"
        group_name = files_directory.rsplit("\\")[-1]

    plt.savefig(plot_folder + "\\" + group_name + "_" + "Clustering_Coefficient_Distribution" + ".png")
    plt.close()
    print("Plot at", plot_folder + "\\" + group_name + "_" + "Clustering_Coefficient_Distribution" + ".png")


# Edge Ranking Table (Comparison)
def edges_rank_comparison(networks, top = 20, plot_folder = None, files_directory = ""):
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
    if files_directory == "":
        if plot_folder is not None:
            group_name = plot_folder + "_"
            plot_folder = config.ROOT + "\\Plots\\SongComparisonOutputFiles\\" + plot_folder
        else:
            plot_folder = ""
    else:
        plot_folder = files_directory + "\\SongGroupAnalysis\\Comparison"
        group_name = files_directory.rsplit("\\")[-1]

    plt.savefig(plot_folder + "\\" + group_name + "_" + "Edge_Rank" + ".png", bbox_inches='tight')
    plt.close()
    print("Plot at", plot_folder + "\\" + group_name + "_" + "Edge_Rank" + ".png")
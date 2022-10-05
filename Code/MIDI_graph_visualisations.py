""" Create Graph representations of specified track of a MIDI file """

import sys
from os import listdir
import os.path

import config
from Plotting import check_dir

import networkx as nx
import matplotlib.pyplot as plt

import mido
import MIDI_general
from Music_Mapping import graph_note_pairs_weighted

# For Community Node-Coloring
import Graph_metrics



def create_graph_vis(G, filename, track_index = None, full_analysis = "", single_file = False, files_directory = "", communities_coloring = False):
    """ Creates a visualisation of a graph through a graph (networkx) object """

    ## Title
    if track_index is None: # If it's not specified the track was the "melody" track
        filename += "_track_" + "melody"
    else:
        filename += "_track_" + str(track_index)
    plt.title(filename)


    """
    Specific parameters for Synthetic_Set_1 graphs to display in the thesis

    straight_fixed_octave_up
    - circular
    - edge label -> label_pos = 0.5

    peak_fixed_octave
    peaks_small_large_constant
    - circular
    - edge label -> label_pos = 0.3


    peaks_small_large_rising
    - spiral -> resolution = 3.00
    - edge label -> label_pos = 0.3

    straight_rising_octave_up
    - spiral -> resolution = 3.00
    - edge label -> label_pos = 0.5


    random_fixed
    random_fully
    - pos = nx.fruchterman_reingold_layout(G, seed = 42, iterations = 50) # Choosing layout with fixed seed
    - edge label -> label_pos = 0.3
    """






    ## Graph
    # pos = nx.fruchterman_reingold_layout(G, seed = 42, iterations = 50) # Choosing layout with fixed seed
    # pos = nx.spiral_layout(G, equidistant = True, resolution = 3.00) # Higher resolution value less compact spiral
    pos = nx.circular_layout(G)


    # pos = nx.kamada_kawai_layout(G)



    plt.figure(figsize=(12,12)) # Increasing canvas' size
    # nx.draw(G, with_labels = True, pos = pos, node_size = 400)
    # nx.draw(G, with_labels = True, pos = pos)
    nx.draw(G, nodelist = [], edgelist = [], with_labels = True, pos = pos) # Not drawing Nodes and Edges because they're already drawn later



    #################
    # Drawing Nodes #
    #################

    ### Setting Node's size as its relative indegree value

    ## Get maximum and minimum value of node degree
    # Initializing both max and min values as the graph's "first" node's in-degree. "First" node of the list created from the directory (which represents the Graph and holds no order)
    min_node_indegree_value = G.in_degree(list(G.nodes)[0], weight = "weight")
    max_node_indegree_value = G.in_degree(list(G.nodes)[0], weight = "weight")
    for node in G.nodes:
        min_node_indegree_value = min(min_node_indegree_value, G.in_degree(node, weight = "weight"))
        max_node_indegree_value = max(max_node_indegree_value, G.in_degree(node, weight = "weight"))



    node_size_min = 200
    node_size_max = 500

    node_sizes = [] # Used to determine edge positioning when drawing edges
    # if len(G.nodes) > 1:

    # Obtaining communities and color list IF it's to color by community
    if communities_coloring:

        # Obtaining communities via Louvain Algorithm
        modularity, communities = Graph_metrics.modularity_louvain(G, list_communities = True)

        list_colors =  ["C"+str(i) for i in range(len(communities))] # Using Matplotlib default color cycle



    if max_node_indegree_value != min_node_indegree_value:
        for node in G.nodes:
            # Current node in-degree
            node_indegree = G.in_degree(node, weight = "weight")

            # Get Node's indegree as a relative value (mapping from [min_value, max_value] to [node_size_min, node_size_max])
            relative_value = node_size_min + (node_size_max - node_size_min)/(max_node_indegree_value - min_node_indegree_value)*(node_indegree - min_node_indegree_value)
            node_sizes.append(relative_value)


            if communities_coloring:
                color = ""
                for i,c in enumerate(communities):
                    if node in c:
                        color = list_colors[i]
                nx.draw_networkx_nodes(G, pos, nodelist = [node], node_size = relative_value, node_color = color, edgecolors = color) # node_color is the fill, edgecolor is the node border
            
            else:
                nx.draw_networkx_nodes(G, pos, nodelist = [node], node_size = relative_value)
                # nx.draw_networkx_nodes(G, pos, nodelist = [node], node_size = relative_value, label = str(node))

        # nx.draw_networkx_labels(G, pos = pos)
    else: # If all nodes have the same in-degree value
        node_fixed_size = int((node_size_max-node_size_min)/2) # Fix size for all nodes
        
        if communities_coloring:
            color = ""
            for i,c in enumerate(communities):
                if node in c:
                    color = list_colors[i]
            nx.draw_networkx_nodes(G, pos, node_size = node_fixed_size, node_color = color, edgecolors = color) # node_color is the fill, edgecolor is the node border
        
        else:
            nx.draw_networkx_nodes(G, pos, node_size = node_fixed_size)
            # nx.draw_networkx_nodes(G, pos, nodelist = [list(G)[0]], node_size = node_fixed_size) # Same as below as it defaults nodelist to list(G)

        node_sizes = [node_fixed_size for i in range(len(list(G.nodes)))] # Setting the same size for all nodes
        # node_sizes.append(node_fixed_size) # Setting the same size for all nodes


    #################
    # Drawing Edges #
    #################


    # https://www.color-hex.com/color-palette/2539
    # Bright to Dark
    red_shades = ["#ffbaba","#ff7b7b","#ff5252","#ff0000","#a70000"]
    num_edge_divisions = len(red_shades)


    # Dictionary that maps edge tuple to its weight
    edge_weights = nx.get_edge_attributes(G, "weight") # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.get_edge_attributes.html

    # [Shades of Red Color Palette](https://www.color-hex.com/color-palette/2539)
    # [get_edge_attributes — NetworkX 2.8.5 documentation](https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.get_edge_attributes.html)


    ## Creating the list that will allow "mapping" each edge, given its weight, to a specific color
    # Initializing min and max value as the weight of the "first" edge when considering the list of edges
    min_edge_weight_value = edge_weights[list(G.edges)[0]]
    max_edge_weight_value = edge_weights[list(G.edges)[0]]

    for edge in G.edges:
        edge_weight = edge_weights[edge]
        min_edge_weight_value = min(min_edge_weight_value, edge_weight)
        max_edge_weight_value = max(max_edge_weight_value, edge_weight)

    edge_interval_length = (max_edge_weight_value - min_edge_weight_value) / num_edge_divisions # The length of each division

    edge_weight_divisons = [] # The list to be used to check to which division/color the edge belongs given its weight
    
    edge_weight_divisons = [min_edge_weight_value + i*edge_interval_length for i in range(num_edge_divisions - 1)]
    edge_weight_divisons.append(max_edge_weight_value)

    ## -----

    for edge in G.edges:
        # Finding the color given its weight. There are num_edge_divisions colors. S
        edge_color = -1
        edge_weight = edge_weights[edge]
        for i in range(len(edge_weight_divisons)):
            if edge_weight < edge_weight_divisons[i]:
                edge_color = i - 1
                break
        # nx.draw_networkx_edges(G, pos, edgelist=[edge], width=edge[2], edge_color = "red")
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color = red_shades[edge_color], node_size = node_sizes, connectionstyle = "arc3, rad=0.15") # node_size isn't used to draw here but to determine edge position
        # For connectionstyle options see https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ConnectionStyle.html#matplotlib.patches.ConnectionStyle

    # Adding edge labels corresponding to the their weight
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weights, label_pos = 0.3, font_size = 8) # For the peaks models
    # nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weights, label_pos = 0.5, font_size = 8)




    ## Exporting to PNG

    if communities_coloring:
        filename += "_communities"

    plot_filename = filename + ".png"
    # if full_analysis == "":
    #     if folder_name == "":
    #         representations_dir = config.ROOT + "\\Music_Graph_Visualisations"
    #     else:
    #         representations_dir = config.ROOT + "\\Music_Graph_Visualisations" + "\\" + folder_name + "_graph_vis"
    # else: # Doing full analysis (Graph visualisation, synthetic representation,...)
    #     representations_dir = full_analysis + "\\Graph_Visualisations"
    
    if full_analysis == "":
        if single_file:
            representations_dir = config.ROOT + "\\Music_Graph_Visualisations"
        else:
            representations_dir = files_directory + "\\Graph_Visualisations"
    else: # Doing full analysis (Graph visualisation, synthetic representation,...)
        representations_dir = full_analysis + "\\Graph_Visualisations"

    check_dir(representations_dir) # Checking if directory folder exists

    if communities_coloring:
        representations_dir += "\\Communities"
        check_dir(representations_dir) # Checking if directory folder exists


    plt.savefig(representations_dir + "\\" + plot_filename)
    plt.close()
    print("Plot at", representations_dir + "\\" + plot_filename)

    return




if __name__ == "__main__":
    if sys.argv[-1][-3:].lower() == "mid": # Run for one specific .mid file
        mid = sys.argv[-1] # The path to the MIDI file given as argument
        mid_file = mido.MidiFile(mid, clip = True)


        ## Get the chosen track
        tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
        filename = MIDI_general.midi_filename(mid_file)
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)

        # Create the graph and its visualisation
        G, notes, notes_duration = graph_note_pairs_weighted(mid_file, track_index = track_index)
        create_graph_vis(G, filename, single_file = True)
    
    else:
        if len(sys.argv) == 1: # Runnning at Code\MIDI_files\synthetic
            print("Running at Code\MIDI_files\synthetic")
            files_directory = config.ROOT + "\\" + "MIDI_files\\synthetic" # Synthetic (generated) files folder
            folder_name = ""

        else: # Points to another directory
            files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are
            folder_name = sys.argv[-1].rsplit("\\")[-1]


        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

        if len(list_files) == 0:
            print("The folder is empty") # No MIDI files
            exit()

        print("Running for the following files:")
        for mid in list_files:
            print(mid)
        print("\n-----\n")

        tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
        for mid in list_files: # Do this for all (.mid) files of the folder
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

            ## Get the chosen track
            filename = MIDI_general.midi_filename(mid_file)
            track_index = MIDI_general.track_from_dict(filename, tracks_indices)

            # Create the graph and its visualisation
            G, notes, notes_duration = graph_note_pairs_weighted(mid_file, track_index = track_index)
            create_graph_vis(G, filename, files_directory = files_directory)

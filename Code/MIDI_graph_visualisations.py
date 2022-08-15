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




def create_graph_vis(G, filename):
    """ Creates a visualisation of a graph through a graph (networkx) object """

    ## Title
    if track_index is None: # If it's not specified the track was the "melody" track
        filename += "_track_" + "melody"
    else:
        filename += "_track_" + str(track_index)
    plt.title(filename)




    ## Graph
    pos = nx.fruchterman_reingold_layout(G, seed = 42, iterations = 50) # Choosing layout with fixed seed

    plt.figure(figsize=(12,12)) # Increasing canvas' size
    # nx.draw(G, with_labels = True, pos = pos, node_size = 400)
    nx.draw(G, with_labels = True, pos = pos)





    # Do something similar to edges' thickness, or maybe color using a color pallete that indicates it


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


    ## TESTING
    print(edge_weight_divisons)
    for i in range(num_edge_divisions):
        print(min_edge_weight_value + i*edge_interval_length, min_edge_weight_value + (i+1)*edge_interval_length)
        # print(min+i*ui,min+(i+1)*ui)
    ## TESTING


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
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color = red_shades[edge_color])



    ### Setting Node's size as its relative indegree value

    ## Get maximum and minimum value of node degree
    # Initializing both max and min values as the graph's "first" node's in-degree. "First" node of the list created from the directory (which represents the Graph and holds no order)
    min_node_indegree_value = G.in_degree(list(G.nodes)[0])
    max_node_indegree_value = G.in_degree(list(G.nodes)[0])
    for node in G.nodes:
        min_node_indegree_value = min(min_node_indegree_value, G.in_degree(node))
        max_node_indegree_value = max(max_node_indegree_value, G.in_degree(node))



    node_size_min = 100
    node_size_max = 500

    for node in G.nodes:
        # Get Node's indegree as a relative value (mapping from [min_value, max_value] to [node_size_min, node_size_max])
        relative_value = node_size_min + (node_size_max - node_size_min)/(max_node_indegree_value - min_node_indegree_value)*(node - min_node_indegree_value)

        nx.draw_networkx_nodes(G, pos, nodelist = [node], node_size = relative_value)




    ## Exporting to PNG
    plot_filename = filename + ".png"
    representations_dir = config.ROOT + "\\Music_Graph_Visualisations"
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
        create_graph_vis(G, filename)
    
    else:
        if len(sys.argv) == 1: # Runnning at Code\MIDI_files\synthetic
            print("Running at Code\MIDI_files\synthetic")
            files_directory = config.ROOT + "\\" + "MIDI_files\\synthetic" # Synthetic (generated) files folder

        else: # Points to another directory
            files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are



        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

        if len(list_files) == 0:
            print("The folder is empty") # No MIDI files
            exit()

        print("Running for the following files:")
        for mid in list_files:
            print(mid)

        tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
        for mid in list_files: # Do this for all (.mid) files of the folder
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

            ## Get the chosen track
            filename = MIDI_general.midi_filename(mid_file)
            track_index = MIDI_general.track_from_dict(filename, tracks_indices)

            # Create the graph and its visualisation
            G, notes, notes_duration = graph_note_pairs_weighted(mid_file, track_index = track_index)
            create_graph_vis(G, filename)

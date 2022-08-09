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


    # for edge in G.edges(data = "weight"):
    #     # nx.draw_networkx_edges(G, pos, edgelist=[edge], width=edge[2], edge_color = "red")
    #     nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color = "red")


    ## Adjust this for edge's weight
    # min_value = list(G.nodes)[0]
    # max_value = list(G.nodes)[0]
    # print(G.nodes(data = True))
    # print(G.nodes(data = "weight"))
    # for node in G:
    #     print(node)
    #     print(int(node))
    #     max_value = max(max_value, node)
    #     min_value = min(min_value, node)





    ### Setting Node's size as its relative indegree value

    ## Get maximum and minimum value of node degree

    # Initializing both max and min values as the graph's "first" node's in-degree. "First" node of the list created from the directory (which represents the Graph and holds no order)
    min_value = G.in_degree(list(G.nodes)[0])
    max_value = G.in_degree(list(G.nodes)[0])
    for node in G:
        max_value = max(max_value, G.in_degree(node))
        min_value = min(min_value, G.in_degree(node))


    # Create a function that takes those two as input and a third which is the node to be changed's in-degree

    node_size_min = 100
    node_size_max = 500

    for node in G.nodes:
        # Get Node's indegree as a relative value (mapping from [min_value, max_value] to [node_size_min, node_size_max])
        relative_value = node_size_min + (node_size_max - node_size_min)/(max_value - min_value)*(node - min_value)

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

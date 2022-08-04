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




# Read simple examples of networkx
# G = nx.Graph()
# G.add_edges_from([(0,1), (0,2), (1,2)])
# nx.draw(G, with_labels = True)

# plt.show()
# G = graph_note_pairs_weighted(mid_file)




## Replicate them
## Create the graph (objet)
## From the graph object create its graph representation (as simple as possible)
# Tweak details

## Allow it in bulk (i.e. choosing a directory)




def create_graph_vis(G, filename):
    """ Creates a visualisation of a graph through a graph (networkx) object """

    nx.draw(G, with_labels = True)




    # Title
    if track_index is None: # If it's not specified the track was the "melody" track
        filename += "_track_" + "melody"
    else:
        filename += "_track_" + str(track_index)


    plot_filename = filename + ".png"
    representations_dir = config.ROOT + "\\Music_Graph_Visualisations"
    check_dir(representations_dir) # Checking if directory folder exists


    ## Exporting to PNG

    plt.savefig(representations_dir + "\\" + plot_filename)
    plt.close()
    print("Plot at", representations_dir + "\\" + plot_filename)

    return




if __name__ == "__main__":
    print("Hello")
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

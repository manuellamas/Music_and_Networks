import networkx as nx
import mido

import sys
import os.path
from os import listdir

import config

import Music_Mapping
import Plotting
import Graph_metrics
import MIDI_general


def graph_display_info(G):
    """ Displays basic info of the created network """
    total_in_degree = 0
    total_out_degree = 0
    for node in G.nodes:
        total_in_degree += G.in_degree(node)
        total_out_degree += G.out_degree(node)


    # Just a simple information "check"
    print("Number of nodes: ", len(G.nodes))
    print("Number of edges: ", G.number_of_edges())

    if isinstance(G,nx.multidigraph.MultiDiGraph):
        # Show number "unique" edges. I.e., how many tuples of notes that are edges exist
        print("Number of 'unique' edges: ", Graph_metrics.multidigraph_unique_edges(G))
        pass
    
    if nx.is_weighted(G,weight="weight"):
        total_weight = 0
        for u, v, weight in G.edges(data="weight"):
            total_weight += weight
        print("Total sum weight: ", total_weight) 
    
    print("Total sum in-degree: ", total_in_degree)
    print("Total sum out-degree: ", total_out_degree)



def create_graphml(network, filename, files_directory, relabel = False):
    """ Create a graphml of a NetworkX network, with or without relabeling of the music note codes """
    if relabel:
        network = nx.relabel_nodes(network, MIDI_general.note_mapping_dict(network)) # Adding labels according to the notes

    dir = files_directory + "\\graphml_files"
    Plotting.check_dir(dir)
    nx.write_graphml(network, dir + "\\" + filename + ".graphml") # Exporting graph to a graphml file

    return



# ----- Main ----- #
if __name__ == "__main__":
    # Python File (Project) Location
    parent_directory = config.ROOT


    # Input
    if len(sys.argv) == 1:
        print("Running sample file")
        file_path = parent_directory + "\\MIDI_files\\LegendsNeverDie.mid"
    else:
        file_path = sys.argv[-1]
        
        if sys.argv[-1][-3:].lower() == "mid": # Run for one specific .mid file
            mid_file = mido.MidiFile(file_path, clip = True)
            # --------------------
            filename = MIDI_general.midi_filename(mid_file) # Getting just the file name (without the path)
            MIDI_general.midi_file_overview(mid_file, filename) # Writing basic info of the midi file to a .txt

            tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
            track_index = MIDI_general.track_from_dict(filename, tracks_indices)
            G, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file, track_index = track_index) #, mid_file.ticks_per_beat) # I'm currently not using the ticks_per_beat might use them in the future

            graph_display_info(G) # Display basic info of the obtained graph
            Plotting.degree_distribution_scatter_plot(G, filename)
            Plotting.edges_rank(G, filename)

            create_graphml(G, filename, relabel = True)



        else: # Run for every MIDI in a folder
            files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

            # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
            list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

            if len(list_files) == 0:
                print("The folder does not have any MIDI files")
                exit()

            print("Running for the following files:")
            for mid in list_files:
                print(mid)

            for mid in list_files:
                mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)
                filename = MIDI_general.midi_filename(mid_file)
            
                tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
                track_index = MIDI_general.track_from_dict(filename, tracks_indices)
            
                G, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file, track_index = track_index) #, mid_file.ticks_per_beat) # I'm currently not using the ticks_per_beat might use them in the future

                create_graphml(G, filename, relabel = True)



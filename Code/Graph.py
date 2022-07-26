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


            # Parsing Input - Command

            # prompt_question = "Weighted or MultiDiGraph? W/M [optional maximum ticks difference]\n"
            # command = input(prompt_question)
            # default_option = False
            # if len(command) != 0:
            #     graph_option = command[0].lower()
            #     while graph_option not in ["m", "w", " ", ""]: # Only accept valid types (or empty) (The whitespace one is to use only time for the interval case)

            #         # The above still needs improvement, for the default case "" I can't just receive a number as it is now. Meaning "26" which would default to "w" with eps=26 currently doesn't work
            #         # REGEX could be a nice way of doing it. Accepting only a number would default to the "m" with interval
            #         command = input(prompt_question)
            #         graph_option = command[0].lower()
            # else: # Default
            #     graph_option = "w"
            #     default_option = True
            # --------------------


            # Obtain the notes and create the graph
            # THIS BELOW NEEDS SOME CLEANING
            # if graph_option == "m": # MultiDigraph

            #     if (len(command) == 1 and command.isalpha()):
            #         G, notes = Music_Mapping.graph_note_multigraph(mid_file)

            #     else: # Same as Simple but with a maximum interval difference between notes
            #         if len(command) > 1:
            #             eps = float(command[2:len(command)])
            #         else:
            #             eps = float(command)
            #         G, notes = Music_Mapping.graph_note_multigraph(mid_file, eps) #, mid_file.ticks_per_beat) # I'm currently not using the ticks_per_beat might use them in the future

            # elif graph_option in ["w", ""]: # Weighted (Default value)
            #     if (len(command) == 1 and command.isalpha()) or default_option:
            #         G, notes = Music_Mapping.graph_note_pairs_weighted(mid_file)

            #     else: # Same as Simple but with a maximum interval difference between notes
            #         if len(command) > 1:
            #             eps = float(command[2:len(command)])
            #         else:
            #             eps = float(command)
            #         G, notes = Music_Mapping.graph_note_pairs_weighted(mid_file, eps) #, mid_file.ticks_per_beat) # I'm currently not using the ticks_per_beat might use them in the future
            # --------------------


            G, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file) #, mid_file.ticks_per_beat) # I'm currently not using the ticks_per_beat might use them in the future

            graph_display_info(G) # Display basic info of the obtained graph
            Plotting.degree_distribution_scatter_plot(G, filename)
            Plotting.edges_rank(G, filename)

            G = nx.relabel_nodes(G, MIDI_general.note_mapping_dict(G)) # Adding labels according to the notes
            nx.write_graphml(G, config.ROOT + "\\graphml_files\\" + filename + ".graphml") # Exporting graph to a graphml file
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
                G, notes, notes_duration = Music_Mapping.graph_note_pairs_weighted(mid_file) #, mid_file.ticks_per_beat) # I'm currently not using the ticks_per_beat might use them in the future

                filename = MIDI_general.midi_filename(mid_file)
                G = nx.relabel_nodes(G, MIDI_general.note_mapping_dict(G)) # Adding labels according to the notes
                nx.write_graphml(G, config.ROOT + "\\graphml_files\\" + filename + ".graphml") # Exporting graph to a graphml file



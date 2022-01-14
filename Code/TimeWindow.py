import networkx as nx
import mido
import numpy as np

import sys
import os.path
from os import listdir

import Music_Mapping
import Graph_metrics
import Plotting
import MIDI_general

def degree_window(mid_file, eps = -1):
    G = nx.DiGraph() # Creating a directed graph
    notes, program = Music_Mapping.get_notes(mid_file, get_track_program = True) # A list with entries as [note, start_time, end_time]
    print(program)
    all_pairs, available_edges = Music_Mapping.get_note_pairs(notes, window = True) # all_edges = [note_1, note_2, note_1_start, note_2_end] ordered by note_1_start
    remaining_edges = [] # This list will serve to hold the edges that weren't added to a graph until this point
    num_pairs = len(all_pairs)

    # NOTES
    # I'm currently not attributing a weight (per window) for each graph, which could be useful later on


    # Fixed Parameters - all time parameters/variables are measured in ticks
    time_interval = 2000 # The amount of ticks per window
    time_skip = 500 # The size of the shift from one window to the next (so there'll be intersection between windows if it's lower than time_interval)

    time_window_start = 0 # Where the window starts (variable)
    current_edges = [] # List of edges of the current 'windowed' graph


    # Graph metrics
    average_degrees = []

    while len(available_edges) != 0:
        edges_to_remove = []


        # ---------- TESTS ----------#
        # print("current_edges")

        # test_edges = current_edges
        # test_edges.sort(key = lambda x:x[0])
        # for edge in test_edges:
        #     print(edge)

        # print("graph edges")
        # graph_edges = list(G.edges())
        # graph_edges.sort(key = lambda x:x[0])
        # for edge in graph_edges:
        #     print(edge)
        # ---------- TESTS End ----------#


        # Removing edges
        for edge in current_edges:
            if edge[2] < time_window_start: # If start is before the start of the window
                G.remove_edge(edge[0], edge[1])
                edges_to_remove.append(edge)

        for edge in edges_to_remove: # Removing from current_edges as well, doesn't work above as it would mess up the for loop the way it is now
            current_edges.remove(edge)

        # Removing edges before adding, because there might be edges that will be removed and then added again. Since an edge is just a connection between two notes, and that connection can appear multiple times (even within the same window).

        # Adding edges
        for edge in available_edges: # Need to check all because an edge could for example strecth out during the whole track
            if edge[2] >= time_window_start and edge[3] <= time_window_start + time_interval:
                # Add edge to the graph, by assigning the two nodes (notes)
                G.add_edge(edge[0], edge[1])

                # Adding edge if there isn't already an edge with the same node values.
                # Because in the same window there can be multiple edges with the same nodes A->B but with different times (but we're ignoring weights for now)
                exists = False
                for existing_edge in current_edges:
                    if existing_edge[0] == edge[0] and existing_edge[1] == edge[1]:
                        exists = True
                        break
                if not exists:
                    current_edges.append(edge)

            elif edge[3] < time_window_start: # Edges that were never entirely on one window, i.e., both notes time have already passed and they were never simultaneously on a time window.
                pass # Ignore those edges
            else:
                remaining_edges.append(edge) # Adding edge for the next windows

        if G.number_of_nodes() != 0:
            average_degrees.append(Graph_metrics.average_degree(G))
        else:
            average_degrees.append(0)

        available_edges = remaining_edges # The available edges are the ones that remain, i.e., that haven't yet been added to a graph
        remaining_edges = []

        time_window_start += time_skip

    # Plotting
    filename = MIDI_general.midi_filename(mid_file)
    Plotting.average_degree_time_window(average_degrees, time_interval, time_skip, filename, program)


    return












if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]

    # Input
    if len(sys.argv) == 1:
        print("Running sample file")
        file_path = parent_directory + "\\MIDI_files\\LegendsNeverDie.mid"
        mid_file = mido.MidiFile(file_path, clip = True)
        degree_window(mid_file)
    elif sys.argv[-1][-3:] == "mid": # Run for one specific .mid file
        file_path = sys.argv[-1]
        mid_file = mido.MidiFile(file_path, clip = True)
        degree_window(mid_file)

    else: # Run for every .mid file in the folder
        files_directory = parent_directory + "\\" + sys.argv[-1] # Where the MIDI files are

        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:]) == "mid"]

        print("Running for the following files:")
        for mid in list_files:
            print(mid)

        for mid in list_files:
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)
            degree_window(mid_file)
import networkx as nx
import mido
import numpy as np

import sys
import os.path

import Music_Mapping
import Graph_metrics
import Plotting
import MIDI_general

def degree_window(mid_file, eps = -1):
    G = nx.DiGraph() # Creating a directed graph
    notes = Music_Mapping.get_notes(mid_file) # A list with entries as [note, start_time, end_time]

    all_pairs, available_edges = Music_Mapping.get_note_pairs(notes, window = True) # all_edges = [note_1, note_2, note_1_start, note_2_end] ordered by note_1_start
    remaining_edges = [] # This list will serve to hold the edges that weren't added to a graph until this point
    num_pairs = len(all_pairs)

    # NOTES
    # I'm currently not attributing a weight (per window) for each graph, which could be useful later on


    # Fixed Parameters - all time parameters/variables are measured in ticks
    time_interval = 1000 # The amount of ticks per window
    time_skip = 100 # The size of the shift from one window to the next (so there'll be intersection between windows if it's lower than time_interval)

    time_window_start = 0 # Where the window starts (variable)
    current_edges = [] # List of edges of the current 'windowed' graph


    # Graph metrics
    average_degrees = []

    while len(available_edges) != 0:
        print(len(available_edges))
        # Removing edges
        for edge in current_edges:
            if edge[2] < time_window_start: # If start is before the start of the window
                G.remove_edge(edge[0], edge[1])

        # Removing edges before adding, because there might be edges that will be removed and then added again. Since an edge is just a connection between two notes, and that connection can appear multiple times (even within the same window).

        # Adding edges
        for edge in available_edges: # Need to check all because an edge could for example strecth out during the whole track
            if edge[2] >= time_window_start and edge[3] <= time_window_start + time_interval:
                # Add edge to the graph, by assigning the two nodes (notes)
                G.add_edge(edge[0], edge[1])
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

        # if len(available_edges) == 66:
        #     print(time_window_start)
        #     print(available_edges[0])
        #     break

    # Plotting
    filename = MIDI_general.midi_filename(mid_file)
    Plotting.average_degree_time_window(average_degrees, time_interval, time_skip, filename)


    return












if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]
    
    # Input
    if len(sys.argv) == 1:
        print("Running sample file")
        file_path = parent_directory + "\\MIDI_files\\LegendsNeverDie.mid"
    else:
        file_path = sys.argv[-1]
    mid_file = mido.MidiFile(file_path, clip = True)


    degree_window(mid_file)
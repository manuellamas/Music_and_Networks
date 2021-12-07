import networkx as nx
import mido
import sys
import os.path
import Music_Mapping
import Plotting
import Graph_metrics

# Separate the info function as a separate file.
# Display basic info of the MIDI file
def midi_file_overview(mid_file, filename):
    file = open("MIDI_file_info.txt", "w")

    file.write(filename+"\n")

    # Information on the MIDI file type
    if mid_file.length == ValueError:
        file.write("MIDI file of type 2, asynchronous")
        midi_type = 2
    elif len(mid_file.tracks) != 1:
        file.write("MIDI file of type 1, synchronous")
        midi_type = 1
    else:
        file.write("MIDI file of type 0, single track")
        midi_type = 0
    file.write("\n")

    # Number of tracks
    if midi_type != 0:
        file.write("Number of tracks: {}" .format(len(mid_file.tracks)))
    
    file.write("\n----------\n\n")

    # Lists all the tracks 'main info'
    for i, track in enumerate(mid_file.tracks):
        file.write("{}: {}\n\n" .format(i,track))

    file.close()



def graph_display_info(G):
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

def midi_filename(mid_file):
    original_file = mid_file.filename
    start = 0
    end = len(original_file) - 1
    for i , s in enumerate(original_file): # It might make more sense using Regex here
        if s == "\\": # Catches the last '\\'
            start = i + 1 # Exactly where the Filename starts
        elif s == ".":
            end = i # One index after the Filename ends
    original_file = original_file[start:end]
    return original_file

# ----- Main ----- #
if __name__ == "__main__":
    # Original File Input
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]

    if len(sys.argv) == 1:
        print("Running sample file")
        file_path = parent_directory + "\\MIDI_files\\LegendsNeverDie.mid"
        # file_path = parent_directory + "\\MIDI_files\\Wikipedia_MIDI_sample.mid"
        # file_path = parent_directory + "\\MIDI_files\\tank.mid"
    else:
        file_path = sys.argv[-1]
    mid_file = mido.MidiFile(file_path, clip = True)
    # --------------------

    original_file = midi_filename(mid_file) # Getting just the file name (without the path)
    midi_file_overview(mid_file, original_file) # Writing basic info of the midi file to a .txt

    # Obtain the notes and create the graph
    prompt_question = "Simple timestamped (with set interval or not) or Weighted? M/W\n"
    command = input(prompt_question)
    if len(command) != 0:
        graph_option = command[0].lower()
        while graph_option not in ["m", "w", " ", ""]: # Only accept valid types (or empty) (The whitespace one is to use only time for the interval case)
            # The above while needs improvement, for "m" case it needs to only be able to receive an integer after it
            # REGEX could be a nice way of doing it. Accepting only a number would default to the "m" with interval
            command = input(prompt_question)
            graph_option = command[0].lower()
    else:
        # Default
        graph_option = "m"
        default_option = True

    notes = Music_Mapping.get_note_pairs(mid_file, graph_option)
    if graph_option in ["m", "", "d"]: # Simple (Default value)
        if len(command) == 1 or default_option:
            G = Music_Mapping.graph_note_pairs_multidigraph(notes)
        else: # Same as Simple but with a maximum interval difference between notes
            eps = int(command[2:len(command)])
            G = Music_Mapping.graph_note_interval(notes, eps, mid_file.ticks_per_beat)
    elif graph_option == "w": # Weighted
        G = Music_Mapping.graph_note_pairs_weighted(notes)

    graph_display_info(G) # Display basic info of the obtained graph
    # Plotting.DegreeDistributionHistogram(G, original_file) # Degree Distribution (Histogram)
    Plotting.DegreeDistributionScatterPlot(G, original_file) # Degree Distribution (Scatter Plot)
    nx.write_graphml(G,"graphml_files\\" + original_file + "_Graph.graphml") # Exporting graph to a graphml file
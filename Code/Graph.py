import networkx as nx
import mido
import sys
import os.path
import Plotting

# Separate the info function as a separate file.
# Display basic info of the MIDI file
def midi_file_overview(mid_file,filename):
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
        file.write("{}: {}" .format(i,track))
        # file.write(i, track)
        # file.write(track[2])
    
    file.close()

def get_notes(mid_file):
    # Dealing with just one track for now, so we automatically pick just the first one (that isn't only MetaMessages)
    if mid_file == "MIDI_files\\MIDI_sample.mid":
        first_track = mid_file.tracks[1] # Starting with 1, not sure what 0 has yet (at least on this Wikipedia sample)
    else:
        first_track = mid_file.tracks[0]

    non_meta_track = 0 # Assuming that the first track isn't only MetaMessages before we check it
    non_meta_track_found = False

    while not non_meta_track_found:
        print(non_meta_track)
        track_is_only_meta = True
        for msg in mid_file.tracks[non_meta_track]:
            if not msg.is_meta:
                track_is_only_meta = False
                break
        if track_is_only_meta:
            non_meta_track += 1
        else:
            non_meta_track_found = True


    first_track = mid_file.tracks[non_meta_track]

    # Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
    notes = []

    for msg in first_track:
        # print("Checking a message")
        if msg.type == "note_on" and msg.velocity != 0:
            notes.append(msg.note)
    return notes

def create_graph_from_notes(notes, file):
    G = nx.DiGraph() # Creating a directed multigraph

    # Count the occurences of pairs of sequential notes
    note_pairs = [] # Elements such as [note1, note2, frequency]
    for i in range(len(notes)-1):
        pair_found = False
        for pair in note_pairs:
            if notes[i] == pair[0] and notes[i+1] == pair[1]: # If the pair has already occurred increased the count
                pair[2] += 1
                pair_found = True
                break
        if not pair_found: # If that pair occurred yet add it to the list
            note_pairs.append([notes[i],notes[i+1],1])

    # Add edges to the graph from the list of pairs that occurred
    for pair in note_pairs:
        G.add_weighted_edges_from([(pair[0],pair[1],pair[2])])

    return G

def graph_display_info(G):
    total_in_degree = 0
    total_out_degree = 0
    for node in G.nodes:
        total_in_degree += G.in_degree(node)
        total_out_degree += G.out_degree(node)

    total_weight = 0
    for u, v, weight in G.edges(data="weight"):
        total_weight += weight

    # Just a simple information "check"
    print("Number of nodes: ", len(G.nodes))
    print("Number of edges: ", len(G.edges))
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
    notes = get_notes(mid_file)
    G = create_graph_from_notes(notes, original_file)

    graph_display_info(G) # Display basic info of the obtained graph
    Plotting.DegreeDistributionHistogram(G, original_file) # Degree Distribution (Histogram)
    nx.write_graphml(G,"graphml_files\\Song_Graph.graphml") # Exporting graph to a graphml file
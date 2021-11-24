import networkx as nx
import mido
import Plotting

G = nx.DiGraph() # Creating a directed multigraph

# mid = mido.MidiFile("MIDI_files/MIDI_sample.mid", clip = True)
# mid = mido.MidiFile("MIDI_files/tank.mid", clip = True)
mid = mido.MidiFile("MIDI_files/LegendsNeverDie.mid", clip = True)


# Display basic info of the MIDI file
def midi_file_overview(mid_file):
    # Information on the MIDI file type
    if mid.length == ValueError:
        print("MIDI file of type 2, asynchronous")
        midi_type = 2
    elif len(mid.tracks) != 1:
        print("MIDI file of type 1, synchronous")
        midi_type = 1
    else:
        print("MIDI file of type 0, single track")
        midi_type = 0

    # Number of tracks
    if midi_type != 0:
        print("Number of tracks: {}" .format(len(mid_file.tracks)))
    
    print("\n----------\n\n")

    # Lists all the tracks 'main info'
    for i, track in enumerate(mid.tracks):
        print(i, track)
        # print(track[2])
    print("\n\n")

def get_notes(mid_file):
    # Dealing with just one track for now, so we automatically pick just the first one (that isn't only MetaMessages)
    if mid_file == "MIDI_files/MIDI_sample.mid":
        first_track = mid.tracks[1] # Starting with 1, not sure what 0 has yet (at least on this Wikipedia sample)
    else:
        first_track = mid.tracks[0]

    non_meta_track = 0 # Assuming that the first track isn't only MetaMessages before we check it
    non_meta_track_found = False

    while not non_meta_track_found:
        print(non_meta_track)
        track_is_only_meta = True
        for msg in mid.tracks[non_meta_track]:
            if not msg.is_meta:
                track_is_only_meta = False
                break
        if track_is_only_meta:
            non_meta_track += 1
        else:
            non_meta_track_found = True


    first_track = mid.tracks[non_meta_track]

    # Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
    notes = []

    for msg in first_track:
        # print("Checking a message")
        if msg.type == "note_on" and msg.velocity != 0:
            notes.append(msg.note)
    return notes

def create_graph_from_notes(notes):

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

    # Degree Distribution (Histogram)
    Plotting.DegreeDistributionHistogram(G)

    # Exporting graph to a graphml file
    nx.write_graphml(G,"graphml_files/Song_Graph.graphml")


# ----- Main ----- #
if __name__ == "__main__":
    # midi_file_overview(mid)

    notes = get_notes(mid)
    create_graph_from_notes(notes)
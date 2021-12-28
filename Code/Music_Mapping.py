import mido
import networkx as nx

# This might not be needed now that melody_track() exists
def first_non_meta_track(mid_file):
    # Ignoring the tracks that only have MetaMessages
    non_meta_track = 0 # Assuming that the first track isn't only MetaMessages before we check it
    non_meta_track_found = False

    while not non_meta_track_found:
        track_is_only_meta = True
        for msg in mid_file.tracks[non_meta_track]:
            if not msg.is_meta:
                track_is_only_meta = False
                break
        if track_is_only_meta:
            non_meta_track += 1
        else:
            non_meta_track_found = True
    return non_meta_track

def melody_track(mid_file):
    """ Returns track with most notes (if multiple chooses the first in file) """
    num_nodes = []
    for track in mid_file.tracks:
        count = 0
        for msg in track:
            if msg.type == "note_on" and msg.velocity != 0: # If a message is "starting" a note
                count += 1
        num_nodes.append(count)
    
    return num_nodes.index(max(num_nodes)) # Returns the first track with the most number of notes


# ---------- Main functions ----------

# ---------- Note Pairs ----------
def get_note_pairs(mid_file, type = "m"):
    # Dealing with just one track for now, so we automatically pick just the first one
    # (that isn't only MetaMessages)
    non_meta_track = melody_track(mid_file)
    first_track = mid_file.tracks[non_meta_track]

    # Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
    notes = []

    if type in ["m", ""]: # MultiDiGraph (Non-weighted) - Default option
        total_time = 0 # Total time since the start of the track. Because 'msg.time' holds only the delta_time (time that passed since last message)
        for msg in first_track:
            if msg.type == "note_on" and msg.velocity != 0: # Creating a node because a note starts
                notes.append([msg.note,total_time,0]) # [note, start_time, end_time]
            
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0): # Editing an existing node to add its "end" timestamp
                for i in range(len(notes)):
                    if notes[i][0] == msg.note and notes[i][2] == 0:
                        notes[i][2] = total_time

            if not msg.is_meta:
                total_time += msg.time

    elif type == "w": # Weighted
        for msg in first_track:
            if msg.type == "note_on" and msg.velocity != 0:
                notes.append(msg.note)

    return notes

# --------------------

# ---------- Graph Creation ----------
# DiGraph weighted
def graph_note_pairs_weighted(notes):
    G = nx.DiGraph() # Creating a directed graph

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
            note_pairs.append([notes[i], notes[i+1], 1])

    # Add edges to the graph from the list of pairs that occurred
    for pair in note_pairs:
        G.add_weighted_edges_from([(pair[0],pair[1],pair[2])])
    return G


# MultiDiGraph (non-weighted)
# This became the default of the graph_notes_interval. Not defining an eps defaults to this graph creation
""" TO BE DELETED """
def graph_note_pairs_multidigraph(notes):
    G = nx.MultiDiGraph() # Creating a directed multigraph

    for i in range(len(notes)-1):
        G.add_edges_from([(notes[i][0], notes[i+1][0])], start = notes[i][1], end = notes[i+1][2])
    return G

# MultiDiGraph (non-weighted) with maximum interval eps between notes
def graph_note_interval(notes, eps = -1): # MultiDiGraph
    """ Creates a Graph where each pair of notes that distance at most eps from each other originate a (directed) edge """
    # def graph_note_interval(notes, eps, ticks_per_beat): # MultiDiGraph
    G = nx.MultiDiGraph() # Creating a directed multigraph

    # Calculate how long is a tick.
    # ticks_per_beat
    # print("One tick is:",)

    if eps == -1:
        for i in range(len(notes)-1):
            G.add_edges_from([(notes[i][0], notes[i+1][0])], start = notes[i][1], end = notes[i+1][2])

    else:
        # List of notes with entries as [note, start_time, end_time]
        for i in range(len(notes)-1):
            if notes[i+1][1] - notes[i][1] <= 1 and notes[i+1][1] - notes[i][1] > 0:
                print(notes[i], notes[i+1])
            if notes[i+1][1] - notes[i][1] < eps: # Only notes that are separated by at most epsilon ticks
                G.add_edges_from([(notes[i][0], notes[i+1][0])], start = notes[i][1], end = notes[i+1][2])

    return G

# --------------------
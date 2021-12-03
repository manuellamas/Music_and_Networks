import mido
import networkx as nx

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

# ---------- Main functions ----------

# ---------- Note Pairs ----------
def get_note_pairs(mid_file, type):
    # Dealing with just one track for now, so we automatically pick just the first one
    # (that isn't only MetaMessages)
    non_meta_track = first_non_meta_track(mid_file)
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

# ---------- Note Pairs - Graph Creation ----------
# MultiDiGraph (non-weighted)
def graph_note_pairs_multidigraph(notes):
    G = nx.MultiDiGraph() # Creating a directed multigraph

    for i in range(len(notes)-1):
        G.add_edges_from([(notes[i][0], notes[i+1][0])], start = notes[i][1], end = notes[i+1][2])
    return G

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

# ---------- Note Interval ----------
def get_note_interval(mid_file, eps, type):


    return notes

# --------------------

# ---------- Note Interval - Graph Creation ----------
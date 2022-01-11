import mido
import networkx as nx

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


# -------------------- Note Pairs Occurrences --------------------
def get_notes(mid_file):
    """ Obtaining a list of the notes of the 'melody track' from a MIDI file (MIDI Object) """
    # Dealing with just one track for now, so we automatically pick the track with the most notes (if there's a tie, the first to occur gets picked)
    melody_track_index = melody_track(mid_file)
    first_track = mid_file.tracks[melody_track_index]

    # Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
    notes = []

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

    return notes # A list with entries as [note, start_time, end_time]

def get_note_pairs(notes, eps = -1, window = False):
    if window:
        # List of edges by time
        edge_time = [] # Will hold every pair (that dists less than eps if it is specified) in a list where each entry is
        # [note_1, note_2, note_1_start, note_2_end]


    note_pairs = [] # Each entry will be of the form [note_1, note_2, #occurrences, times] where times will be a list of the form [ [start_a, end_a], [start_b, end_b], ...] ] ('a' being the first occurrence, 'b' the second and so on)
    for i in range(len(notes) - 1):
        pair_found = False
        if eps == -1 or (notes[i+1][1] - notes[i][1] < eps): # Only notes that are separated by at most epsilon ticks
            for pair in note_pairs:
                if pair[0] == notes[i][0] and pair[1] == notes[i+1][0]:
                    pair[2] += 1 # Increasing the frequency count
                    pair[3].append([notes[i][1], notes[i+1][2]]) # Adding the first note's starting time and last note's ending time, as the start and end of this edge occurrence
                    pair_found = True
            if not pair_found: # If that pair doesn't yet exist add it to the list
                note_pairs.append([notes[i][0], notes[i+1][0], 1, [[notes[i][1], notes[i+1][2]]]])

        if window: # Sliding Window
            edge_time.append([notes[i][0], notes[i+1][0], notes[i][1], notes[i+1][2]])

    if window:
        return note_pairs, edge_time
    else:
        return note_pairs


# ------------------------------------------------------------




# -------------------- Graph Creation --------------------
# DiGraph Weighted
def graph_note_pairs_weighted(mid_file, eps = -1):
    """ Creates a (Simple Directed) Graph where each pair of notes that distance at most eps from each other originate a (directed) edge """
    G = nx.DiGraph() # Creating a directed graph
    notes = get_notes(mid_file) # Obtaining a list of notes, each entry of the list is of the form
    # [note, start_time, end_time]



    note_pairs = get_note_pairs(notes, eps = -1)



    for pair in note_pairs:
        G.add_weighted_edges_from([(pair[0], pair[1], pair[2])]) # Leaving the time out for now

    return G


# MultiDiGraph (non-weighted) with an (optional) maximum interval eps between notes
# Not using it for now since it doesn't work with "common" algorithms metrics
def graph_note_multigraph(mid_file, eps = -1): # MultiDiGraph
    """ Creates a Graph where each pair of notes that distance at most eps from each other originate a (directed) edge """

    G = nx.MultiDiGraph() # Creating a directed multigraph
    notes = get_notes(mid_file)

    # def graph_note_multigraph(notes, eps, ticks_per_beat): # MultiDiGraph
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

# ------------------------------------------------------------
















#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#################### DEPRECATED ####################
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

def get_note_pairs_DEPRECATED(mid_file, type = "w"):
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
        total_time = 0 # Total time since the start of the track. Because 'msg.time' holds only the delta_time (time that passed since last message)

        for msg in first_track:
            # This was the entirety of the previous function
            # if msg.type == "note_on" and msg.velocity != 0:
            #     notes.append(msg.note)
            # ----------------------------------------------

            if msg.type == "note_on" and msg.velocity != 0: # Creating a node because a note starts
                notes.append([msg.note,total_time,0]) # [note, start_time, end_time]
            
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0): # Editing an existing node to add its "end" timestamp
                for i in range(len(notes)):
                    if notes[i][0] == msg.note and notes[i][2] == 0:
                        notes[i][2] = total_time

            if not msg.is_meta:
                total_time += msg.time

    return notes

def graph_note_pairs_weighted_DEPRECATED(notes):
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
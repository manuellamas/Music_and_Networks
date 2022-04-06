import networkx as nx
from MIDI_general import midi_filename, melody_track, SHORTREST_NOTE, LONGREST_NOTE




# -------------------- Obtaining list of notes --------------------
def get_notes(mid_file , get_track_program = False, track_index = None):
    """ Obtaining a list of the notes from a specific track from a MIDI file (MIDI Object)
    which if not specified will just be the 'melody track' """

    if track_index is None:
        # Dealing with just one track for now, so we automatically pick the track with the most notes (if there's a tie, the first to occur gets picked)
        melody_track_index = melody_track(mid_file)
        first_track = mid_file.tracks[melody_track_index]
    else:
        first_track = mid_file.tracks[track_index]
    # Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
    notes = []

    program = None # The first program_change declaration of the track (if it exists)

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

        if get_track_program and msg.type == "program_change":
            program = msg.program

    if get_track_program:
        if program is not None:
            return notes, program # Returning the program (instrument) used in the track, assuming only one program is used. If there's more than one for now we only keep the last
        else:
            filename = midi_filename(mid_file) # Getting just the file name (without the path)
            print("The track of the song: " + filename + " has no Program")
    return notes # A list with entries as [note, start_time, end_time]



def merge_tracks(mid_file):
    """ Merge all tracks notes from a MIDI file into a single (ordered list) """

    all_notes = [] # Contains all notes from the previously analyzed tracks
    merge_all_notes = [] # List were notes from both all_notes and track_notes are being merged. Is created on each iteration
    track_notes = [] # Notes of the track currently being analyzed

    # Add the first track's notes directly in merge_all_notes
    first_track = 0 # Index of first track with notes (i.e. not a "Meta" track)
    all_notes = get_notes(mid_file, track_index = first_track)
    while len(all_notes) == 0 and first_track < len(mid_file.tracks) - 1:
        first_track += 1
        all_notes = get_notes(mid_file, track_index = first_track)

    for track_index in range(1 + first_track, len(mid_file.tracks)): # Adding all tracks of a song one by one
        track_notes = get_notes(mid_file, track_index = track_index)

        new_track_pointer = 0 # Pointer to the next note to analyze in the new track - tracks_notes
        all_notes_pointer = 0 # Pointer to the next note to analyze in all_notes

        # Analyze both track_notes and all_notes with a pointer in each (for the starting time of a node)
        # and add note instances to all notes by moving along both track_notes and all_notes simultaneously
        # Add the notes (smaller starting time first) on all_notes

        while new_track_pointer < len(track_notes) and all_notes_pointer < len(all_notes):
            if track_notes[new_track_pointer][1] < all_notes[all_notes_pointer][1]:
                merge_all_notes.append(track_notes[new_track_pointer])
                new_track_pointer += 1

            else: # if all_notes note occurs earlier OR at the same time
                merge_all_notes.append(all_notes[all_notes_pointer])
                all_notes_pointer += 1


        while new_track_pointer < len(track_notes): # Add track_notes notes if we haven't yet gone through the whole list
            merge_all_notes.append(track_notes[new_track_pointer])
            new_track_pointer += 1

        while all_notes_pointer < len(all_notes): # Add all_notes notes if we haven't yet gone through the whole list
            merge_all_notes.append(all_notes[all_notes_pointer])
            all_notes_pointer += 1


        # Update the list
        all_notes = merge_all_notes
        merge_all_notes = [] # Reset the list for the next iteration

    return all_notes
# -------------------- Obtaining list of notes End --------------------






# ------------ Obtaining pairs of consecutive notes from the list of notes ------------
def get_note_pairs(notes, eps = -1, window = False):
    """ Getting a list of note pairs (with occurrences number and times) """
    if window:
        # List of edges by time
        edge_time = [] # Will hold every pair (that dists less than eps if it is specified) in a list where each entry is
        # [note_1, note_2, note_1_start, note_2_end]

    notes_duration = []

    # ----- Working with Rests (Creating them as a node) -----
    interval_between_notes = [] # Time from a note ending to the next one beginning. Each entry i will correspond to the "space" between notes i and i+1
    minimum_duration = notes[0][2] - notes[0][1]
    maximum_duration = notes[0][2] - notes[0][1]

    for i in range(len(notes) - 1):
        interval_between_notes.append(notes[i+1][1] - notes[i][2]) # Time from a note ending to the next one beginning

        duration = notes[i][2] - notes[i][1] # Duration of the note
        minimum_duration = min(minimum_duration, duration)
        maximum_duration = max(maximum_duration, duration)

        notes_duration.append(duration) # Creating a list with all notes durations to work with as a song's feature


    # ----- Working with Rests End -----

    note_pairs_rest = [] # Similar to note_pairs but making only the pairs between a rest (short or long) and a note. And of the form [note_1, note_2, #occurrences]
    note_pairs = [] # Each entry will be of the form [note_1, note_2, #occurrences, times] where times will be a list of the form [ [start_a, end_a], [start_b, end_b], ...] ] ('a' being the first occurrence, 'b' the second and so on)
    for i in range(len(notes) - 1):
        pair_found = False # Pair from note to note

        pair_note_rest_found = False # Pair from note to rest
        pair_rest_note_found = False # Pair from rest to note

        short_rest = False # If it exists a short rest between the two notes
        long_rest = False # If it exists a long rest between the two notes

        if eps == -1 or (notes[i+1][1] - notes[i][1] < eps): # Only notes that are separated by at most epsilon ticks
            if interval_between_notes[i] > minimum_duration: # Will be considered as a rest
                if interval_between_notes[i] < maximum_duration: # It's a Short Rest - Code 128
                    short_rest = True
                else:
                    long_rest = True

            if not short_rest and not long_rest: # There is no rest between notes
                for pair in note_pairs:
                    if pair[0] == notes[i][0] and pair[1] == notes[i+1][0]:
                        pair[2] += 1 # Increasing the frequency count
                        pair[3].append([notes[i][1], notes[i+1][2]]) # Adding the first note's starting time and last note's ending time, as the start and end of this edge occurrence
                        pair_found = True
                if not pair_found: # If that pair doesn't yet exist add it to the list
                    note_pairs.append([notes[i][0], notes[i+1][0], 1, [[notes[i][1], notes[i+1][2]]]])

            else: # There is a rest
                if short_rest:
                    rest_value = SHORTREST_NOTE
                else:
                    rest_value = LONGREST_NOTE

                # Checking pair note -> rest
                for pair in note_pairs_rest:
                    if pair[0] == notes[i][0] and pair[1] == rest_value:
                        pair[2] += 1 # Increasing the frequency count
                        pair_note_rest_found = True
                if not pair_note_rest_found: # If that pair doesn't yet exist add it to the list
                    note_pairs_rest.append([notes[i][0], rest_value, 1])

                # Checking pair rest -> note
                for pair in note_pairs_rest:
                    if pair[0] == rest_value and pair[1] == notes[i][1]:
                        pair[2] += 1 # Increasing the frequency count
                        pair_rest_note_found = True
                if not pair_rest_note_found: # If that pair doesn't yet exist add it to the list
                    note_pairs_rest.append([rest_value, notes[i+1][0], 1])





        if window: # Sliding Window
            edge_time.append([notes[i][0], notes[i+1][0], notes[i][1], notes[i+1][2]])

    if window:
        return note_pairs + note_pairs_rest, notes_duration, edge_time
    else:
        return note_pairs + note_pairs_rest, notes_duration

# ------------ Obtaining pairs of consecutive notes from the list of notes End ------------






# -------------------- Graph Creation --------------------
# DiGraph Weighted
def graph_note_pairs_weighted(mid_file, eps = -1):
    """ Creates a (Simple Directed) Graph where each pair of notes that distance at most eps from each other originate a (directed) edge """
    G = nx.DiGraph() # Creating a directed graph

    # # Working with single track
    # notes = get_notes(mid_file) # Obtaining a list of notes, each entry of the list is of the form
    # # [note, start_time, end_time]

    # Working with all tracks by "merging" the notes into a single (ordered) list
    notes = merge_tracks(mid_file)

    note_pairs, notes_duration = get_note_pairs(notes, eps)

    for pair in note_pairs:
        G.add_weighted_edges_from([(pair[0], pair[1], pair[2])]) # Leaving the time out for now

    return G, notes, notes_duration




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

    return G, notes

# ------------------------------------------------------------








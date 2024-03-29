import networkx as nx
from MIDI_general import midi_filename, melody_track, SHORTREST_NOTE, LONGREST_NOTE


# Without these thresholds there were too many rests which overshadowed the notes themselves.
# With graphs becoming centered around the rest notes (128 and 129)

SHORT_REST_THRESHOLD_MULTIPLIER = 200  # 100_000 Multipler of minimum note's duration - Only count as rests intervals whose duration is above the minimum times this threshold and below the maximum times REST_MAX
LONG_REST_THRESHOLD_MULTIPLIER = 1 # Multipler of maximum note's duration - Only count as long rests intervals whose duration is above the maximum times this threshold
REST_MAX_MULTIPLIER = 5 # Multiplier of maximum note's duration - Rests (short and long) can only have at most maximum duration times this multiplier

MINIMUM_DURATION_VALUE = 1 # To prevent it being 0 causing every interval to originate a rest

# -------------------- Obtaining list of notes --------------------
def get_notes(mid_file , get_track_program = False, track_index = None, ticks = False):
    """ Obtaining a list of the notes from a specific track from a MIDI file (MIDI Object)
    Returns a list with entries as [note, start_time, end_time] """



    if track_index is None:
        # Dealing with just one track for now, so we automatically pick the track with the most notes (if there's a tie, the first to occur gets picked)
        melody_track_index = melody_track(mid_file)
        first_track = mid_file.tracks[melody_track_index]
    else:
        first_track = mid_file.tracks[track_index]
    # Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
    notes = []

    program = None # The first program_change declaration of the track (if it exists)

    total_ticks = 0 # Total time (in ticks) since the start of the track. Because 'msg.time' holds only the delta_time (time that passed since last message)
    for msg in first_track:

        if msg.type == "note_on" and msg.velocity != 0: # Creating a node because a note starts
            notes.append([msg.note, total_ticks + msg.time, 0]) # [note, start_time, end_time]
        
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0): # Editing an existing node to add its "end" timestamp
            for i in range(len(notes)):
                if notes[i][0] == msg.note and notes[i][2] == 0:
                    notes[i][2] = total_ticks + msg.time

        if not msg.is_meta:
            total_ticks += msg.time

        if get_track_program and msg.type == "program_change":
            program = msg.program


    ## Currently get_track_program and ticks CANNOT be both simultaneously True ##

    if get_track_program:
        if program is not None:
            return notes, program # Returning the program (instrument) used in the track, assuming only one program is used. If there's more than one for now we only keep the last
        else:
            filename = midi_filename(mid_file) # Getting just the file name (without the path)
            print("The track of the song: " + filename + " has no Program")

    if not ticks:
        return notes # A list with entries as [note, start_time, end_time].
    else:
        return notes, total_ticks # A list with entries as [note, start_time, end_time]. And total_time being the total number of ticks of the song



def get_notes_rest(mid_file, track_index = None):
    """ Get list of notes with rests 
    Returns list with notes values only """

    notes, total_ticks = get_notes(mid_file, track_index = track_index, ticks = True)

    ## Getting the minimum and maximum note's duration to attribute to the Short Rest and Long Rest respectively
    # Attributing as a start to both min and max values the first note's duration
    min_duration = notes[0][2] - notes[0][1] # The duration of the smallest note's duration
    max_duration = notes[0][2] - notes[0][1] # The duration of the longest note's duration

    for note in notes:
        duration = note[2] - note[1] # Note's duration
        min_duration = min(min_duration, duration)
        max_duration = max(max_duration, duration)
    min_duration = max(MINIMUM_DURATION_VALUE, min_duration) # It must be at least 1


    ## Going through the notes and adding rests
    final_notes = []
    for i in range(len(notes) - 1):
        final_notes.append(notes[i][0])

        interval_duration = notes[i+1][1] - notes[i][2] # Obtaining the interval duration between consecutive notes

        if interval_duration > min_duration * SHORT_REST_THRESHOLD_MULTIPLIER and interval_duration < max_duration * REST_MAX_MULTIPLIER:
            if interval_duration > max_duration * LONG_REST_THRESHOLD_MULTIPLIER: # Long Rest
                final_notes.append(LONGREST_NOTE)
            else: # Short Rest
                final_notes.append(SHORTREST_NOTE)

    # Adding last note
    final_notes.append(notes[-1][0])


    return final_notes # List with notes values only (but including rests)



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

    minimum_duration = max(MINIMUM_DURATION_VALUE, minimum_duration) # It must be at least 1

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
            if interval_between_notes[i] > minimum_duration * SHORT_REST_THRESHOLD_MULTIPLIER and interval_between_notes[i] < maximum_duration * REST_MAX_MULTIPLIER: # Will be considered as a rest
                if interval_between_notes[i] < maximum_duration * LONG_REST_THRESHOLD_MULTIPLIER: # It's a Short Rest - Code 128
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
def graph_note_pairs_weighted(mid_file, eps = -1, ticks = False, track_index = None):
    """ Creates a (Simple Directed) Graph where each pair of notes that distance at most eps from each other originate a (directed) edge """
    G = nx.DiGraph() # Creating a directed graph

    # # Working with single track
    notes, total_ticks = get_notes(mid_file, ticks =  True, track_index = track_index) # Obtaining a list of notes, each entry of the list is of the form
    # [note, start_time, end_time]

    if len(notes) == 1: # If there's only one node, since it won't create edges, create the single node
        G.add_node(notes[0][0])

    # Working with all tracks by "merging" the notes into a single (ordered) list
    # notes = merge_tracks(mid_file)

    note_pairs, notes_duration = get_note_pairs(notes, eps)

    for pair in note_pairs:
        G.add_weighted_edges_from([(pair[0], pair[1], pair[2])]) # Leaving the time out for now
        # By Default weight gets added as
        # weight = "weight"

    if not ticks:
        return G, notes, notes_duration
    else:
        return G, notes, notes_duration, total_ticks



# ------------------------------------------------------------








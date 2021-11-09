import networkx as nx
import mido

G = nx.DiGraph() # Creating a directed multigraph

mid = mido.MidiFile("MIDI_files/MIDI_sample.mid", clip = True)
# print(mid)

# Lists all the tracks 'main info'
# for track in mid.tracks:
#     print(track[0])

# Dealing with just one track for now
first_track = mid.tracks[1] # Starting with 1, not sure what 0 has yet (at least on this Wikipedia sample)

first_track = first_track[1:-1] # Cut off the first and last entries of the list


# Add each note to a list by order of "occurrence". For now I'm just using time of "note_on" of the note
notes = []

for msg in first_track:
    if msg.type == "note_on" and msg.velocity != 0:
        notes.append(msg.note)

# Count the occurences of pairs of sequential notes
note_pairs = [] # Elements such as [node1, note2, frequency]
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


print(G.in_degree[45])
print(G.out_degree[45])

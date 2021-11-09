import networkx as nx
import mido

G = nx.MultiDiGraph() # Creating a directed multigraph

mid = mido.MidiFile("MIDI_files/MIDI_sample.mid", clip = True)

# print(mid)

# Lists all the tracks 'main info'
# for track in mid.tracks:
#     print(track[0])

# Dealing with just one track for now
first_track = mid.tracks[1] # Starting with 1, not sure what 0 has yet (at least on this Wikipedia sample)

first_track = first_track[1:-1] # Cut off the first and last entries of the list

for msg in first_track:
    if msg.type == "note_on" and msg.velocity != 0:
        print(msg.note)

# Create a graph that has the above notes as nodes and edges between each of them.
# Not sure how it works if it has the same "name" which will be the notes themselves, but it should work weel as a multigraph. Meaning it should add only one node per note.
# What happens when I add a node with the same name (note)? Does it ignore or does it create a double?
# Maybe I should just add the edges and then create the notes from those edges, I saw that was possible.

# Also, make this a github repo
#### Requirements
[NetF](https://github.com/vanessa-silva/NetF) on the Code\Music_NetF folder.



### Music mapping (to a graph)
#### First version
The graph is being created by looking only at each note's start. Meaning *I'm currently ignoring the velocity and duration*.
A note x comes after another note y if it's start comes immediately after it. If that happens there will be a directed link from note x -> y.

I'm reverting to using a "Simple" Digraph, meaning not a multidigraph as several algorithms don't work with it.
#### Timestamps
For the use of the "sliding window", I'll have an ordered list of each edge, where each entry will also have when time edge starts and ends. Which will correspond to the first note's starting time and last note's ending time.

# Usage
**Note** 30/11/2021: As of now, it'll probably not work on all files. And even in those that it does the created graph is still crude. It only looks at a single track and therefore the graph isn't by any means a faithful representation of the song.

It currently only looks at the track with the most nodes (if there are multiple tracks with that number of notes then it chooses the first)

File Input Style:
- `py Code/Graph.py <file>`

Command Input Style:
- `[m/M] <max_time_between_notes>` where `<max_time_between_notes>` is optional (and is in *ticks* which is a bit tricky to define in seconds, as the ticks can change throughout the song)
- `[w/W]`

### Basic Usage
Running `Graph.py` file from the project root folder (`<root>`). (So `py Code/Graph.py`)
This will work on a sample MIDI file.

You'll be prompted with *"MultiDiGraph (timestamped and unweighted) or Digraph Weighted? M/W"*.
- `m` will create a MultiDiGraph where each instance of pair of notes found will form an edge with two timestamp attributes (`start` and `end`, the starting time of the first note and end time of the second note).
- `w` will create a DiGraph where between two (ordered) nodes (and thus notes) there can only be at most one edge

The reply is case-insensitive, `m` and `M` will give the same result.
An empty reply defaults to the `m` case.


It'll:
- Create a (NetworkX) `graph` object
- Export `graph` to a `<root>\graphml_files\Song_Graph.graphml` file, to be used with Gephi (for example)
- Create a `<root>\MIDI_file_info.txt` which contains basic MIDI file info as well as all the tracks and messages
- Create a `<root>\Plots\Degree_Distribution_ScatterPlot_<file_name>.png` image which contains the degree distribution of the created `graph` object

#### Other files
If an argument is given, it'll create the graph for the specified MIDI file
`py Code/Graph.py <path_to_file>`






# Notes
*How should I approach rounding when calculating Betwenness and Closeness centrality?*
If I don't round almost all values are different, but if I round too much I lose too much information.

Check betwenness centrality, using or not `"weight"` attribute.
Similarly in closeness centrality with the `distance = "weight"`
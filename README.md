### Music mapping (to a graph)
#### First version
The graph is being created by looking only at each note's start. Meaning *I'm currently ignoring the velocity and duration*.
A note x comes after another note y if it's start comes immediately after it. If that happens there will be a directed link from note x -> y.


# Usage
**Note** 30/11/2021: As of now, it'll probably not work on all files. And even in those that it does the created graph is still crude. It only looks at a single track and therefore the graph isn't by any means a faithful representation of the song.

### Basic Usage
Running `Graph.py` file from the project root folder.
This will work on a sample MIDI file.

It'll:
- Create a (NetworkX) `graph` object
- Export `graph` to a `<root>\graphml_files\Song_Graph.graphml` file, to be used with Gephi (for example)
- Create a `<root>\MIDI_file_info.txt` which contains basic MIDI file info as well as all the tracks and messages
- Create a `<root>\Plots\Degree_Distribution_<file_name>.png` image which contains the degree distribution of the created `graph` object

#### Other files
If an argument is given, it'll create the graph for the specified MIDI file
`Graph.py <path_to_file>`
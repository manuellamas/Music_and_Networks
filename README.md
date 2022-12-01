### Datasets
The datasets used in the thesis are present in the `Thesis_Datasets` directory.

#### Requirements
Requirements include [Mido](https://mido.readthedocs.io/en/latest/), [NetworkX ](https://networkx.org/), and [NumPy](https://numpy.org/).

All requirements are saved in the `requirements.txt` file, present in the project root folder.

### Main project
#### Overview
To get an overview of a specific MIDI file run `py Code\MIDI_general.py <path-to-song>`
A file will be created (or modified if it already exists) `MIDI_file_info.txt` and it'll show all messages (per track) of the MIDI file.


#### Analysis
Running the command `py Code\Full_Group_Analysis.py <path-to-songs-directory>` where `<path-to-songs-directory>` is a directory with MIDI files will:
- (A series of subfolders will be created in the specified directory)
- Create a graph from each MIDI file, if the MIDI file contains several tracks, the track with the higher number notes will be chosen
  - The specific track can be chosen beforehand by writing the filename and track number separated by a space in the file `Chosen_Tracks.txt` (located on the root of the project folder)
  - The created graphs will be exported to graphml (which can then be used in specific programs to handle networks such as Gephi) on the subfolder `graphml_files`
- Create feature analysis (table with feature values of the graphs mapped from the MIDI) present in the subfolder `FeatureAnalysis`
  - can be invoked by itself with `py Code\Feature_Analysis.py <path-to-songs-directory>`
- Create both time series and graph representations of each file of the chosen directory, in subfolders named respectively `Time_Series_Representation` and `Graph_Visualisations`
  - can be invoked by itself with `py Code\MIDI_synthetic_representations.py <path-to-songs-directory>` for time series representation
  - can be invoked by itself with `py Code\MIDI_graph_visualisations.py <path-to-songs-directory>` for graph representation
- Create a table presenting clustering results (from *k*-means) in subfolder `SongGroupAnalysis`
  - as well as create a degree distribution plot and edge rank table for each song in `SongGroupAnalysis\Single`
  - can be invoked by itself with `py Code\SongGroupAnalysis.py <path-to-songs-directory>`


### Extra
Many of the present MIDI files (and even Code sections or files) ended up not being used for the results present in the thesis.
One of which was `Code\SongGroupAnalysisNetF.py` that resorted to a different set of features created using the tool [NetF](https://github.com/vanessa-silva/NetF)
To run that script the NetF code present on the mentioned repository must exist as a subfolder on the `Code\Music_NetF` folder.


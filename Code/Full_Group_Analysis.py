""" 
Running the following programs on the specified file or folder:
And creating a folder for each on the original file or folder's directory for easier access

- Graph Visualisations
- Time series representation / Synthetic representation
- Splitting Tracks
- SongGroup Analysis
- Single Song Plots
# SongComparison (for the whole)
(Might add) Graphml through SongGroup Analysis (just change where it's created)
"""



import sys
from os import listdir
import os.path
from Plotting import check_dir

import mido
import MIDI_general
import config

from Music_Mapping import graph_note_pairs_weighted
from MIDI_graph_visualisations import create_graph_vis
from MIDI_synthetic_representations import plot_all_tracks
from MIDI_tracks import midi_split_tracks
from SongGroupAnalysis import main_analysis
from SongComparison import main_song_comparison_plots
import Plotting

def print_section_title(section):
    """ To improve readability on command line output (prints) """
    l = len(section)
    left_side = "\n\n" + (l + 4) * "#" + "\n" + "# "
    right_side = left_side[::-1]
    
    print(left_side + section + right_side)
    return




if __name__ == "__main__":
    import time
    start_time = time.time()



    if sys.argv[-1][-3:].lower() == "mid": # Run for one specific .mid file
        mid = sys.argv[-1] # The path to the MIDI file given as argument
        mid_file = mido.MidiFile(mid, clip = True)


        ## Get the chosen track
        tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
        filename = MIDI_general.midi_filename(mid_file)
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)

        new_dir = mid.replace(".mid", "") + "_Analysis"
        check_dir(new_dir)

        # Create the graph and its visualisation
        G, notes, notes_duration = graph_note_pairs_weighted(mid_file, track_index = track_index)
        create_graph_vis(G, filename, track_index = track_index, full_analysis = new_dir, single_file = True)

        # Time series representation
        plot_all_tracks(mid_file, with_rests = True, full_analysis = new_dir)

        # Split Tracks
        midi_split_tracks(mid_file, full_analysis = new_dir)

    else:
        if len(sys.argv) == 1: # Runnning at Code\MIDI_files\synthetic
            print("Running at Code\MIDI_files\synthetic")
            files_directory = config.ROOT + "\\" + "MIDI_files\\synthetic" # Synthetic (generated) files folder
            folder_name = ""

        else: # Points to another directory
            files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are
            folder_name = sys.argv[-1].rsplit("\\")[-1]


        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

        if len(list_files) == 0:
            print("The folder is empty") # No MIDI files
            exit()

        print("Running for the following files:")
        for mid in list_files:
            print(mid)
        print("\n-----\n")

        tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
        for mid in list_files: # Do this for all (.mid) files of the folder
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

            ## Get the chosen track
            filename = MIDI_general.midi_filename(mid_file)
            track_index = MIDI_general.track_from_dict(filename, tracks_indices)
            print_section_title(filename)

            # Create the graph and its visualisation
            G, notes, notes_duration = graph_note_pairs_weighted(mid_file, track_index = track_index)
            create_graph_vis(G, filename, track_index = track_index, full_analysis = files_directory)

            # Time series representation
            plot_all_tracks(mid_file, with_rests = True, full_analysis = files_directory)

            # Split Tracks
            midi_split_tracks(mid_file, full_analysis = files_directory)

            # Graph Metrics Plots
            Plotting.degree_distribution_scatter_plot(G, filename, files_directory)
            Plotting.edges_rank(G, filename, files_directory)

        # Song Group Analysis (k-means)
        print_section_title("Song Group Analysis")
        main_analysis(files_directory)

        # Song Comparison Plots
        print_section_title("Song Comparison Plots")
        main_song_comparison_plots(files_directory)



    print("\n\n----- %s seconds -----" % (time.time() - start_time))
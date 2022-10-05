
import sys
import os.path
from os import listdir

import config

import mido

import MIDI_general
import Music_Mapping
from Plotting import check_dir

import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

# The y column should have all the notes that are present (without repettion)
# The x should have the starting and ending ticks of each one, no need for any other but keep them well in the line
# i.e. the scale must be linear 1, , , 4, 5, and not 1,4,5


def create_timeline_bar(mid_file, track_index, files_directory, filename):
    """ Creating a timeline bar for a MIDI """

    notes = Music_Mapping.get_notes(mid_file, track_index = track_index) # A list with entries as [note, start_time, end_time]


    # Saving lists of notes and their times for the ticks and mapping
    list_times = []

    list_notes = []
    for n in notes:
        list_notes.append(n[0]) # Note code
        list_times.append(n[1]) # Start time of a note
        list_times.append(n[2]) # End time of a note


    # Sort list given each elements' first occurrence position
    list_times = list(set(list_times))
    list_times.sort()

    list_notes = list(set(list_notes))
    list_notes.sort()


    # Associating a color with each existing note
    colormapping = {}
    # color_list = ["#ffb300", "#803e75", "#ff6800", "#a6bdd7", "#c10020", "#cea262", "#817066"]

    for i, unique_value in enumerate(list_notes):
        # colormapping[unique_value] = color_list[i]
        colormapping[unique_value] = "C" + str(i) # Using Matplotlib's default color cycle https://matplotlib.org/3.5.1/tutorials/colors/colors.html#:~:text=default%20color%20cycle Convert to RGBA to see exactly which ones they are


    verts = []
    colors = []

    half_size = .3

    for n in notes:
        v =  [(n[1], n[0] - half_size),
            (n[1], n[0] + half_size),
            (n[2], n[0] + half_size),
            (n[2], n[0] - half_size),
            (n[1], n[0] - half_size)]
        verts.append(v)
        colors.append(colormapping[n[0]])


    bars = PolyCollection(verts, facecolors=colors)

    fig, ax = plt.subplots()
    ax.add_collection(bars)
    ax.autoscale()
    
    fig.set_size_inches(6.4, 4.8, forward=True) # Defining the figure/window size
    plt.subplots_adjust(bottom = 0.17)

    # Xticks
    # ax.set_xticks(list_times)
    ax.tick_params(axis = "x", labelrotation = 90)

    # Yticks
    ax.set_yticks(list_notes)

    # Axis Labels
    ax.set_xlabel('Ticks', labelpad = 9) # labelpad padding between the label and the ticks
    ax.set_ylabel('MIDI note codes', labelpad = 6)
    # ax.set_xlabel('Ticks', labelpad = 9, fontsize = 14) # labelpad padding between the label and the ticks
    # ax.set_ylabel('MIDI note codes', labelpad = 6, fontsize = 14)

    # Ticks Text Size
    # ax.tick_params(axis='both', which='major', labelsize = 14)

    ax.spines[['top', 'right']].set_visible(False) # Hides right and top axis


    # Export
    if files_directory[-3:].lower() == "mid":
        files_directory = files_directory.rsplit("\\",1)[0]

    export_directory = files_directory + "\\Timeline_Bar"
    check_dir(export_directory)

    export_directory += "\\" + filename + "_timeline_bar" + ".png"

    # plt.savefig(export_directory, bbox_inches='tight')
    plt.savefig(export_directory)
    plt.close()
    print("Plot at", export_directory)

    return



def batch_timeline_bar(files_directory):
    """ Creating a timeline bar for a set of MIDIs """

    # Obtain a list of the file names of all MIDI files in the directory (SongArena by Default). Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]
    list_files.sort() # Sorts the list alphabetically


    tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
    print("\n-----\nChosen Tracks:\n")


    for mid in list_files:
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        filename = MIDI_general.midi_filename(mid_file)
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)

        create_timeline_bar(mid_file, track_index, files_directory, filename)
        

    return





if __name__ == "__main__":
    # Directory Target
    if len(sys.argv) == 1:
        print("Running at Song Arena")
        files_directory = config.ROOT + "\\SongArena" # Where the MIDI files to be analyzed are
        batch_timeline_bar(files_directory)

    elif len(sys.argv) == 2:
        if sys.argv[-1][-3:].lower() == "mid": # A single MIDI
            pass

            file_directory = config.ROOT + "\\" + sys.argv[-1] # The path to the MIDI file
            tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand

            mid_file = mido.MidiFile(file_directory, clip = True)
            filename = MIDI_general.midi_filename(mid_file)
            track_index = MIDI_general.track_from_dict(filename, tracks_indices)

            create_timeline_bar(mid_file, track_index, file_directory, filename)

        else: # A directory
            files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are
            batch_timeline_bar(files_directory)

    else:
        print("Too many arguments")
        exit()



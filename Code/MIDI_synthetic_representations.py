import sys
from os import listdir
import os.path

import config
import matplotlib.pyplot as plt
from Plotting import check_dir

import mido
import MIDI_general
from Music_Mapping import get_notes, get_notes_rest




#######################
## Support functions ##
#######################


def get_midi_note_list(mid_file, with_rests = True, track_index = None):
    """
    Obtain list of notes from a MIDI file
    working on the "Melodic" Track
    """

    series = []

    if with_rests:
        notes_with_rests = get_notes_rest(mid_file, track_index = track_index) # Obtain a list of notes with rests. VALUES ONLY
        for note in notes_with_rests:
            series.append(note) # When working with rests, we get only the value

    else:
        notes = get_notes(mid_file, track_index = track_index) # Obtaining a list of notes, each entry of the list is of the form [note, time_start, time_end]
        for note in notes:
            series.append(note[0]) # note[0] corresponds to just the note (and not the times)

    return series



##############
## Plotting ##
##############

def format_y_ticks(value, tick_number):
    print(value)
    if int(value) == float(value):
        MIDI_general.midi_num_to_note(int(value))
    else:
        return value



def plot_all_tracks(mid_file, with_rests = True):
    """ Plots the representation of all tracks of a MIDI file """
    for track_index, track in enumerate(mid_file.tracks):

        empty_track = True
        for msg in track: # Checking if the track isn't empty
            if msg.type == "note_on" and msg.velocity != 0: # If a message is "starting" a note
                empty_track = False
                break

        if not empty_track:
            plot_track(mid_file, with_rests = True, track_index = track_index)



def plot_track(mid_file, with_rests = True, track_index = None):
    """ Plots a representation of a MIDI file specific track (the melody one if not specified) """
    fig, ax = plt.subplots()

    note_list = get_midi_note_list(mid_file, with_rests, track_index) # Note list
    filename = MIDI_general.midi_filename(mid_file) # Getting the filename

    note_order = [i for i in range(1, len(note_list) + 1)] # Just the order of the notes. 1,2,3,...
    # note_list being the notes numbers


    # Scatter Plot
    ax.scatter(note_order, note_list, s = 10, label = filename)
    
    # Continuous line
    # ax.plot(note_order, note_list)


    # ylim = [0,127] # Without rests
    ylim = [0,129] # With rests
    # ylim = [0,12]
    ymargin = (ylim[1]-ylim[0])/90
    ax.set_ylim([ylim[0] - ymargin, ylim[1] + ymargin])

    ax.set_yticks(ylim)

    # locs = ax.get_xticks()
    # ax.set_yticks(locs, [midi_num_to_note(int(value)) for value in locs])



    ## Design
    # ax.legend(loc = "upper right")

    # Title
    if track_index is None: # If it's not specified the track was the "melody" track
        filename += "_track_" + "melody"
    else:
        filename += "_track_" + str(track_index)

    # title = "Representation of " + filename
    plt.title(filename)


    # Axis Labels
    ax.set_xlabel('Order')
    ax.set_ylabel('Note')


    # Legend
    # plt.legend(loc="upper left")



    plot_filename = filename + ".png"
    representations_dir = config.ROOT + "\\Music_Representations"
    check_dir(representations_dir) # Checking if directory folder exists


    ## Exporting to PNG


    plt.savefig(representations_dir + "\\" + plot_filename)
    print("Plot at", representations_dir + "\\" + plot_filename)

    return











if __name__ == "__main__":
    # Input
    if sys.argv[-1][-3:].lower() == "mid": # Run for one specific .mid file
        mid = sys.argv[-1] # The path to the MIDI file given as argument
        mid_file = mido.MidiFile(mid, clip = True)

        # plot_track(mid_file, with_rests = True)
        plot_all_tracks(mid_file, with_rests = True)
    
    else:
        if len(sys.argv) == 1: # Runnning at Code\MIDI_files\synthetic
            print("Running at Code\MIDI_files\synthetic")
            files_directory = config.ROOT + "\\" + "MIDI_files\\synthetic" # Synthetic (generated) files folder

        else: # Points to another directory
            files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are



        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

        if len(list_files) == 0:
            print("The folder is empty") # No MIDI files
            exit()

        print("Running for the following files:")
        for mid in list_files:
            print(mid)

        tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
        for mid in list_files: # Do this for all (.mid) files of the folder
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

            ## To plot just one track
            # filename = MIDI_general.midi_filename(mid_file)
            # track_index = MIDI_general.track_from_dict(filename, tracks_indices)
            # plot_track(mid_file, with_rests = True)

            plot_all_tracks(mid_file, with_rests = True)



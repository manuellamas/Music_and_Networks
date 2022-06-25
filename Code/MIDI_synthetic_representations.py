import sys
from os import listdir
import os.path

import config
import matplotlib.pyplot as plt
from Plotting import check_dir

import mido
from MIDI_general import midi_filename, midi_num_to_note
from Music_Mapping import get_notes




#######################
## Support functions ##
#######################


def get_midi_note_list(mid_file):
    """ Obtain list of notes from a MIDI file (with a single non-meta Track) """

    notes = get_notes(mid_file) # Obtaining a list of notes, each entry of the list is of the form [note, time_start, time_end]

    series = []
    for note in notes:
        series.append(note[0]) # note[0] corresponds to just the note (and not the times)

    return series



##############
## Plotting ##
##############

def format_y_ticks(value, tick_number):
    print(value)
    if int(value) == float(value):
        midi_num_to_note(int(value))
    else:
        return value



def plot_track(note_list, filename):
    fig, ax = plt.subplots()

    note_order = [i for i in range(1, len(note_list) + 1)] # Just the order of the notes. 1,2,3,...
    # note_list being the notes numbers


    # Scatter Plot
    ax.scatter(note_order, note_list, s = 10, label = filename)
    
    # Continuous line
    # ax.plot(note_order, note_list)


    ylim = [0,127]
    # ylim = [0,12]
    ymargin = (ylim[1]-ylim[0])/90
    ax.set_ylim([ylim[0] - ymargin, ylim[1] + ymargin])

    ax.set_yticks(ylim)

    # locs = ax.get_xticks()
    # ax.set_yticks(locs, [midi_num_to_note(int(value)) for value in locs])



    ## Design
    # ax.legend(loc = "upper right")

    # title = "Representation of " + filename
    plt.title(filename)

    # Axis Labels
    ax.set_xlabel('Order')
    ax.set_ylabel('Note')

    # Legend
    # plt.legend(loc="upper left")

    plot_filename = filename + ".png"
    representations_dir = config.ROOT + "\\Synthetic_Representations"
    check_dir(representations_dir) # Checking if directory folder exists

    plt.savefig(representations_dir + "\\" + plot_filename)
    print("Plot at", representations_dir + "\\" + plot_filename)

    return


# Start by plotting consecutive ups on the same octave

# Get the list of notes from the MIDI's I created, and do a scatter plot of it to start with.
# What scale should I do it on? For now I'll make just from 0 to 12 (giving margins so that 0 and 12 are not on the borders)








if __name__ == "__main__":
    # Input
    if len(sys.argv) == 1: # Runnning at Code\MIDI_files\synthetic
        print("Running at Code\MIDI_files\synthetic")
        files_directory = config.ROOT + "\\" + "MIDI_files\\synthetic" # Synthetic (generated) files folder
    
    else: # Point to another directory
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are



    # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

    if len(list_files) == 0:
        print("The folder is empty") # No MIDI files
        exit()

    print("Running for the following files:")
    for mid in list_files:
        print(mid)

    for mid in list_files: # Do this for all (.mid) files of the folder
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        note_list = get_midi_note_list(mid_file) # Note list
        filename = midi_filename(mid_file) # Getting the filename
        plot_track(note_list, filename)


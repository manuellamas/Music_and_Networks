""" Get information from musics in a folder """

import sys
import config
from os import listdir
import os.path

import mido
import MIDI_general
from Music_Mapping import graph_note_pairs_weighted

from tabulate import tabulate



def music_number_of_notes(files_directory):
    """ Output a file with number of notes of each music in the directory """
    # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
    list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]


    file = open(files_directory + "\\" + "_Num_notes.txt", "w") # file is the file path and mode can be w(rite)/r(ead)/a(ppend)

    # Maybe do the same for length (minutes) ?
    # [MIDI Files — Mido 1.2.10 documentation](https://mido.readthedocs.io/en/latest/midi_files.html?highlight=length#playback-length)

    list_notes = []

    # Create graph for each
    tracks_indices = MIDI_general.get_chosen_tracks() # A dictionary mapping MIDI filenames to a track chosen by hand beforehand
    for mid in list_files: # Do this for all (.mid) files of the folder
        mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)

        ## Get the chosen track
        filename = MIDI_general.midi_filename(mid_file)
        track_index = MIDI_general.track_from_dict(filename, tracks_indices)

        # Create the graph and its visualisation
        G, notes, notes_duration = graph_note_pairs_weighted(mid_file)
        # G, notes, notes_duration = graph_note_pairs_weighted(mid_file, track_index = track_index)
    
        # Get number of notes from each
        num_notes = len(notes)

        list_notes.append([filename, num_notes])

    list_notes.sort(key = lambda s: s[1], reverse = True)

    file.write(tabulate(list_notes, headers=['Song', '# Notes']))
    file.close()

    return











if __name__ == "__main__":
    # Directory Target
    if len(sys.argv) == 2:
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

    else:
        print("A directory was not given")
        exit()




    music_number_of_notes(files_directory)




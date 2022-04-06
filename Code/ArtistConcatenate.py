""" To use for genre clustering """

import os.path
from os import listdir
import Music_Mapping
from MIDI_general import SHORTREST_NOTE, LONGREST_NOTE

# -------- #
# UNTESTED #
# -------- #

def merge_artist(artist_directory):
    """ Concatenates several songs into a single list with the notes. (Currently using all tracks of a song) """

    list_files = [f for f in listdir(artist_directory) if os.path.isfile(os.path.join(artist_directory, f))]
    list_midi_files = [f for f in list_files if f[-4:] == ".mid"]

    merged_list = []

    for midi_file in list_midi_files:
        all_notes = Music_Mapping.merge_tracks(midi_file) # Using all tracks of the song
        merged_list += all_notes

        # Adding a Long Rest between songs
        merged_list += LONGREST_NOTE

    return merged_list
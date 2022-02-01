""" General MIDI functions """

import pandas as pd
import mido

import os.path
import sys

def midi_file_overview(mid_file, filename):
    """ Exports into a txt file type, number of tracks, and the MIDI Messages themselves """
    file = open("MIDI_file_info.txt", "w")

    file.write(filename+"\n")

    # Information on the MIDI file type
    if mid_file.length == ValueError:
        file.write("MIDI file of type 2, asynchronous")
        midi_type = 2
    elif len(mid_file.tracks) != 1:
        file.write("MIDI file of type 1, synchronous")
        midi_type = 1
    else:
        file.write("MIDI file of type 0, single track")
        midi_type = 0
    file.write("\n")

    # Number of tracks
    if midi_type != 0:
        file.write("Number of tracks: {}" .format(len(mid_file.tracks)))
    
    file.write("\n----------\n\n")

    # Lists all the tracks 'main info'
    for i, track in enumerate(mid_file.tracks):
        file.write("{}: {}\n\n" .format(i,track))

    file.close()



def midi_filename(mid_file):
    """ A function that takes a path to midi file and returns just the file's name """
    original_file = mid_file.filename
    start = 0
    end = len(original_file) - 1
    for i , s in enumerate(original_file): # It might make more sense using Regex here
        if s == "\\": # Catches the last '\\'
            start = i + 1 # Exactly where the Filename starts
        elif s == ".":
            end = i # One index after the Filename ends
    original_file = original_file[start:end]
    return original_file



# MIDI program
def midi_program_num_to_name(program, instrument = False):
    # Program Category
    if program in list(range(0,8)):
        program_category = "Piano"
    elif program in list(range(8,16)):
        program_category = "Chromatic percussion"
    elif program in list(range(16,24)):
        program_category = "Organ"
    elif program in list(range(24,32)):
        program_category = "Guitar"
    elif program in list(range(32,40)):
        program_category = "Bass"
    elif program in list(range(40,48)):
        program_category = "Strings"
    elif program in list(range(48,56)):
        program_category = "Ensemble"
    elif program in list(range(56,64)):
        program_category = "Brass"
    elif program in list(range(64,72)):
        program_category = "Reed"
    elif program in list(range(72,80)):
        program_category = "Pipe"
    elif program in list(range(80,88)):
        program_category = "Synth lead"
    elif program in list(range(88,96)):
        program_category = "Synth pad"
    elif program in list(range(96,104)):
        program_category = "Synth effects"
    elif program in list(range(104,112)):
        program_category = "Ethnic"
    elif program in list(range(112,120)):
        program_category = "Percussive"
    elif program in list(range(120,128)):
        program_category = "Sound effects"


    if instrument:
        # Python File (Project) Location
        program_directory = os.path.dirname(__file__) # Where the Python script being ran is

        csv_file = pd.read_csv(program_directory + "\\Data\\MIDI_Program_Names.csv", header = None)
        program_list = csv_file[0].to_list() # 0 because it's the first (and only) column

        program_instrument = program_list[program]




    if instrument:
        return program_category, program_instrument
    else:
        return program_category



# MIDI Note
def midi_num_to_note(note_code):
    # Checking if the number is not on the table
    if note_code < 0 or note_code > 127:
        print("The note code doesn't represent any note (in any octave)")
        return

    octave = [str(i) for i in range(-1,10)]
    note =  ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    return octave[note_code // 12] + note[note_code % 12]




if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]

    file_path = sys.argv[-1]
    mid_file = mido.MidiFile(file_path, clip = True)

    filename = midi_filename(mid_file)
    midi_file_overview(mid_file, filename)
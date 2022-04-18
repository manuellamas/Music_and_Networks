""" Working with a MIDI file (song) as a Time Series """

import sys
import os.path
from os import listdir
import config
import mido

from MIDI_general import midi_filename
from Music_Mapping import get_notes
import Plot.Plotting_Time_Series as plt_time_series

# Create a (ordered) list, using the melodic track, which will be the time series
def series_from_MIDI (mid_file):
    """ Create list (series) from MIDI """
    
    notes = get_notes(mid_file) # Obtaining a list of notes, each entry of the list is of the form [note, time_start, time_end]
    
    series = []
    for index, note in enumerate(notes):
        series.append([note[0],index]) # Adding as a list (with index) in case I use in the future series that aren't uniformly spaced

    print(series)
    return series



if __name__ == "__main__":
    # Input
    if len(sys.argv) == 1:
        print("Running sample file")
        file_path = config.ROOT + "\\MIDI_files\\LegendsNeverDie.mid"
        mid_file = mido.MidiFile(file_path, clip = True)
        series = series_from_MIDI(mid_file)

        # Plotting
        filename = midi_filename(mid_file)
        plt_time_series.simple_time_series_plot(series, filename)

    elif sys.argv[-1][-3:].lower() == "mid": # Run for one specific .mid file
        file_path = sys.argv[-1]
        mid_file = mido.MidiFile(file_path, clip = True)
        series = series_from_MIDI(mid_file)

        # Plotting
        filename = midi_filename(mid_file)
        plt_time_series.simple_time_series_plot(series, filename)

    else: # Run for every .mid file in the folder
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

        if len(list_files) == 0:
            print("The folder is empty")
            exit()

        print("Running for the following files:")
        for mid in list_files:
            print(mid)

        for mid in list_files:
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)
            series = series_from_MIDI(mid_file)

            # Plotting
            filename = midi_filename(mid_file)
            plt_time_series.simple_time_series_plot(series, filename)
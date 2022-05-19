""" Working with a MIDI file (song) as a Time Series """

import sys
import os.path
from os import listdir
import config
import mido
import csv
import subprocess


from MIDI_general import midi_filename
from Music_Mapping import get_notes
import Plot.Plotting_Time_Series as plt_time_series

# Create a (ordered) list, using the melodic track, which will be the time series
def series_from_MIDI (mid_file):
    """ Create list (series) from MIDI """

    notes = get_notes(mid_file) # Obtaining a list of notes, each entry of the list is of the form [note, time_start, time_end]
    
    series = []
    for note in notes:
        series.append(note[0])


    # Export Time Series list "series" to an CSV
    with open("Code/Music_NetF/time_series.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(series)

    # Running the R Script that works with NetF
    res = subprocess.call("rscript Code/Music_NetF/MusicTimeSeriesNetFeatures.R", shell=True)

    # Import Time Series Network Features (NetF) from an CSV
    with open("Code/Music_NetF/netf_feature_list.csv", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ",")

        rows = []
        for row in csv_reader:
            rows.append(row)

        network_features = rows[1] # The first row is the name of each feature

    return network_features



def series_from_MIDI_group(mid_file_list):
    """ Create list (series) from MIDI - but gives as input several files at once """
    # Meaning it only needs to run Rscript once


    all_series = [] # List of all time series (one per each midi file)

    for mid_file in mid_file_list:
        notes = get_notes(mid_file) # Obtaining a list of notes, each entry of the list is of the form [note, time_start, time_end]
        
        series = []
        for note in notes:
            series.append(note[0])

        all_series.append(series)


    # Export All Time Series list "series" to an CSV - Each Series on a line/row
    with open("Code/Music_NetF/time_series_group.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(len(mid_file_list)): # Writing one time series per line
            csv_writer.writerow(all_series[i])

    # Each series on a column



    # Running the R Script that works with NetF
    res = subprocess.call("rscript Code/Music_NetF/MusicTimeSeriesNetFeaturesGroup.R", shell=True)

    # Import Time Series Network Features (NetF) from an CSV
    with open("Code/Music_NetF/netf_group_feature_list.csv", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ",")

        rows = []
        for row in csv_reader:
            rows.append(row)

        network_features = rows[1:] # The first row is the name of each feature

    return network_features



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
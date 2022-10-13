import mido

import sys
import os.path
from os import listdir
from Plotting import check_dir
from MIDI_general import *

import config






def midi_split_tracks(mid_file, folder_path = "", full_analysis = ""):
    """ Creates a MIDI file per non meta track in the original MIDI """


    # melody_track_index = melody_track(mid_file)
    # print("The chosen track was:", melody_track_index)
    meta_track_index = first_meta_track(mid_file)
    # new_mid = mido.MidiFile()

    if meta_track_index is not None: # Adding a MetaTrack (if it exists)
        new_meta_track = mido.MidiTrack()
        # new_mid.tracks.append(new_meta_track)

        meta_track = mid_file.tracks[meta_track_index]
        for msg in meta_track:
            new_meta_track.append(msg)

    # print("Meta track is", meta_track_index)
    # for i, track in enumerate(mid_file.tracks):
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         print(msg)

    # print("\n\n-----\n\n")

    if full_analysis == "":
        if folder_path == "":
            split_tracks_dir = config.ROOT + "\\Split_Tracks"
        else:
            split_tracks_dir = config.ROOT + "\\Split_Tracks\\" + folder_path
    else: # Doing full analysis (Graph visualisation, synthetic representation,...)
        split_tracks_dir = full_analysis + "\\Split_Tracks"

    
    check_dir(split_tracks_dir)

    print("Tracks split at", split_tracks_dir)

    for i, track in enumerate(mid_file.tracks):
        new_mid = mido.MidiFile()

        if check_is_track_meta(track): # If the track doesn't contain any note_on or note_off messages, the track will not be created as a separate MIDI
            continue

        if meta_track_index is not None:
            if i == meta_track_index: continue # Don't create a MIDI for the meta track
            new_mid.tracks.append(new_meta_track) # Add the meta track to all other new MIDIs

        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)

        for msg in track:
            new_track.append(msg)

        filename = midi_filename(mid_file)

        new_mid.save(split_tracks_dir + "\\" + filename + "_track" + str(i).zfill(2) + ".mid")
        # new_mid.save("Split_Tracks\\" + filename + "_track" + str(i).zfill(2) + ".mid")

    return




if __name__ == "__main__":
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    parent_directory = os.path.split(program_directory)[0]

    # try:
    if sys.argv[-1][-3:].lower() == "mid": # Run for one specific .mid file

        file_path = sys.argv[-1]
        mid_file = mido.MidiFile(file_path, clip = True)

        filename = midi_filename(mid_file)
        midi_file_overview(mid_file, filename)

        # midi_get_track(mid_file)
        midi_split_tracks(mid_file)
    else: # Run for all MIDI in a folder
        files_directory = config.ROOT + "\\" + sys.argv[-1] # Where the MIDI files are

        folder_path = sys.argv[-1].rsplit("\\")[-1]

        # Obtain a list of the file names of all MIDI files in the directory specified. Only those in the "root" and not in a subdirectory
        list_files = [f for f in listdir(files_directory) if (os.path.isfile(os.path.join(files_directory, f)) and f[-3:].lower() == "mid")]

        if len(list_files) == 0:
            print("The folder does not have any MIDI files")
            exit()

        print("Running for the following files:")
        for mid in list_files:
            print(mid)

        for mid in list_files:
            mid_file = mido.MidiFile(files_directory + "\\" + mid, clip = True)
        
            # midi_get_track(mid_file)
            midi_split_tracks(mid_file, full_analysis = files_directory)

    # except:
    #     print("No path to a MIDI or Folder was provided")
    #     print("Check if 'Split_Tracks' folder exists at Root")
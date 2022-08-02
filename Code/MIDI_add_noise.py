"""
Adding noise to existing MIDI files
"""

import mido
import random
from numpy import sign
import sys
from MIDI_general import midi_filename

def add_noise(mid, percentage = 0.1, max_deviation = 5, track_to_add_noise_index = 1):
    """
    Adding noise to a certain percentage of notes
    Incrementing or decrementing the value by at most max_deviation
    (But considering the normal limits of 0-127)
    """

    # New midi file that will have noise
    mid_noise = mido.MidiFile(type = 1)

    # meta_track = mido.MidiTrack() # Track with values and settings
    # mid_noise.tracks.append(meta_track)
    ## Copy the meta_track from the original file

    # track = mido.MidiTrack() # Track with the actual notes
    # mid_noise.tracks.append(track)
    # Should I get a list of notes, or just change each message as I go?
    # If it's as I go I need to at least get the number of messages (notes) to get the number of notes I'll change through the percentage


    for i, track in enumerate(mid.tracks):

        if i == track_to_add_noise_index:
            empty_track = True
            for msg in track:
                if msg.type == "note_on" and msg.velocity != 0: # If a message is "starting" a note
                    empty_track = False
                    break

            # emtpy_track and a lot of this code can probably be replaced by a try and except

            if empty_track: # If the track to add noise is doesn't have any notes
                print("The track to add noise is empty.")
                quit()
            else:
                track = add_noise_to_track(track, percentage, max_deviation)


        mid_noise.tracks.append(track)

    # Saving the file
    title = midi_filename(mid)
    new_title = title + "_noise" + "_p_" + str(percentage).ljust(4,"0") + "_md_" + str(max_deviation)

    mid_path = "MIDI_files/synthetic/" + new_title + ".mid"
    mid.save(mid_path)
    print("Added noise to MIDI", title)
    print("Noise file is", new_title)


def add_noise_to_track(track, percentage = 0.1, max_deviation = 5):
    """ Adds noise to a track """
    num_notes = 0 # Number of notes in this track

    list_msg = [] # List of msg indices

    checkpoint = 0 # Last note instance index, on list_msg, that already has both start and stop message indices

    for i, msg in enumerate(track):

        if msg.type == "note_on" and msg.velocity != 0: # If a message is "starting" a note
            list_msg.append([msg.note, i])

        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0): # Adding the index to the "ending" message of a note
            for j in range(checkpoint, len(list_msg)):
                if list_msg[j][0] == msg.note and len(list_msg[j]) == 2:
                    list_msg[j].append(i)
                    checkpoint += 1 # Increasing the checkpoint so that on future checks it only needs to start further ahead, as the previous ones are complete (with start and end indices)

    # Obtaining the number of notes, and the number of notes to add noise
    num_notes = len(list_msg)
    num_notes_noise = int(num_notes * percentage)

    indices_to_add_noise = random.sample(range(num_notes), num_notes_noise) # List of note indices to add noise 


    # for i in range(num_notes_noise):
    for i in indices_to_add_noise: # going through the indices of the list with entries note, start, end
        message_on = track[list_msg[i][1]]
        message_off = track[list_msg[i][2]]


        note_value = message_on.note
        # I need to have the note's value to be able to know how far up/down I can increase/decrease
 
        note_value - 5

        # Specifying the most we can subtract without going below the allowable note value 0
        if note_value - max_deviation < 0:
            max_decrement = - note_value
        else:
            max_decrement = - max_deviation


        # Specifying the most we can add without going over the allowable note value 127
        if note_value + max_deviation > 127:
            max_increment = 127 - note_value
        else:
            max_increment = max_deviation


        note_noise = random.randint(max_decrement, max_increment)

 
        message_on.note += note_noise
        message_off.note += note_noise



    return track





if __name__ == "__main__":

    if sys.argv[1][-3:].lower() == "mid": # Run for one specific .mid file
        mid = sys.argv[1] # The path to the MIDI file given as argument
        mid_file = mido.MidiFile(mid, clip = True)

        if len(sys.argv) == 2:
            add_noise(mid_file)

        else: # If parameters were specified
            percentage = sys.argv[2]
            max_deviation = sys.argv[3]
            add_noise(mid_file, percentage, max_deviation)
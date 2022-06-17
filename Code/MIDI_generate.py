""" Generating Synthetic MIDI files with specific characteristics to test our analysis """

import mido
import random


def midi_synthetic(midi_generator, **args):
    """ Generate a MIDI file for testing """

    # New midi file
    mid = mido.MidiFile(type = 1)

    meta_track = mido.MidiTrack() # Track with values and settings
    mid.tracks.append(meta_track)

    track = mido.MidiTrack() # Track with the actual notes
    mid.tracks.append(track)

    # Meta track
    meta1 = mido.MetaMessage("time_signature", numerator = 4, denominator = 4, clocks_per_click = 24, notated_32nd_notes_per_beat = 8, time = 0)
    meta_track.append(meta1)
    
    meta2 = mido.MetaMessage('set_tempo', tempo = 361445, time = 0)
    meta_track.append(meta2)



    # Specifying the track name
    track_name_message = mido.MetaMessage("track_name", name = "Ragtime Piano")
    track.append(track_name_message)

    # Specifying the program
    program_message = mido.Message("program_change", channel = 0, program = 3, time = 0)
    track.append(program_message)



    ### Specifying what to generate (and getting the title)
    title = midi_generator(track, **args) # This is adding messages to the main track via an inputed function



    # Saving the file
    mid_path = "MIDI_files/synthetic/" + title + ".mid"
    mid.save(mid_path)
    
    return





##################################################
#------------------------------------------------#
##################################################
# Generators

# Choose an even number of REPETITIONS (For, for example, the up down up down sequences)
REPETITIONS = 6






def midi_fixed_note(track, note = 1, times = REPETITIONS*12):
    """ Keeps playing the same note """
    
    repeat(track, note, times)

    return "fixed_note" + "_" + str(note).zfill(3) # zfill pads the number to have three digits



def midi_repeat_aabb(track, starting_note = 0, last_note = 11, up = True):
    """
    Repeating the same note n times until going through the entire octave
    DO DO ... DO RE RE ... RE ...
    Or the same but starting on the highest note
    """

    if up:
        range_interval = range(starting_note, last_note + 1)
    else:
        range_interval = reversed(range(starting_note, last_note + 1))

    for i in range_interval:
        repeat(track, i, REPETITIONS)

    if up:
        return "repeat_aabb_up"
    else:
        return "repeat_aabb_down"



#########################
## Straight Up or Down ##
#########################

def midi_straight_rising_octave(track, starting_note = 0, last_note = (12*REPETITIONS - 1), up = True):
    """
    Do Re Mi ... - going up to different octaves
    OR
    ... Mi Re Do - going down to different octaves
    """

    straight(track, starting_note, last_note, up)

    if up:
        return "straight_rising_octave_up"
    else:
        return "straight_rising_octave_down"



def midi_straight_fixed_octave(track, starting_note = 0, last_note = 11, up = True):
    """ Do Re Mi ... Do - on a loop up at a fixed octave """

    for j in range(REPETITIONS):
        straight(track, starting_note, last_note, up)
    
    if up:
        return "straight_fixed_octave_up"
    else:
        return "straight_fixed_octave_down"




#######################
## Peaks and Valleys ##
#######################

def midi_peak_fixed_octave(track, starting_note = 0, peak_height = 11):
    """
    Straight up and down on the same octave
    Do Re Mi ... Do - on a loop down at a fixed octave
    """

    for j in range(REPETITIONS):
        peak(track, starting_note, peak_height)

    return "peak_fixed_octave"



def midi_small_large_peaks_constant(track, starting_note = 0, small_peak_height = 5, large_peak_height = 11):
    """ 
    Small peak, large peak, on a loop
    """

    for j in range(REPETITIONS):
        peak(track, starting_note, small_peak_height) # Small Peak
        peak(track, starting_note, large_peak_height) # Large Peak

    return "peaks_small_large_constant"



def midi_small_large_peaks_rising(track, starting_note = 0, small_peak_height = 5, large_peak_height = 11, step = 5):
    """
    Small peak, large peak ending above (by step) the initial point
    Then loop
    Making it have a up tendency
    """

    for j in range(REPETITIONS):
        peak(track, starting_note, small_peak_height) # Small Peak
        peak(track, starting_note, large_peak_height) # Large Peak

    return "peaks_small_large_rising"



############
## Random ##
############

random.seed(42)

def midi_random_fixed_octave(track, starting_note = 0, last_note = 11):
    """
    Random notes within a fixed octave
    It's only on a fixed octave depending on the values of starting_note and last_note
    """
    for i in range(REPETITIONS*12):
            random_note = random.randint(starting_note, last_note) # Random number between starting_note and last_note (including)

            message_on = mido.Message('note_on', note = random_note, velocity = 50, time = 20)
            track.append(message_on)

            message_off = mido.Message('note_off', note = random_note, velocity = 50, time = 300)
            track.append(message_off)

    return "random_fixed_octave"



def midi_fully_random(track):
    """ Fully random notes """
    for i in range(REPETITIONS*12):
            random_note = random.randint(0, 127) # Random number between 0 and 127 (including)

            message_on = mido.Message('note_on', note = random_note, velocity = 50, time = 20)
            track.append(message_on)

            message_off = mido.Message('note_off', note = random_note, velocity = 50, time = 300)
            track.append(message_off)

    return "random_fully"





##################################################
#------------------------------------------------#
##################################################
# Supporting Functions

def straight(track, starting_note = 0, last_note = 11, up = True):
    """ Steadily go up (or down) from starting_note until last_note """

    if up:
        range_interval = range(starting_note, last_note + 1)
    else:
        range_interval = reversed(range(starting_note, last_note + 1))

    for i in range_interval:
            message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
            track.append(message_on)

            message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
            track.append(message_off)

    return



def repeat(track, note_to_repeat = 0, times = 1):
    """ Repeats the same note a specific number of times """

    for i in range(times):
        message_on = mido.Message('note_on', note = note_to_repeat, velocity = 50, time = 20)
        track.append(message_on)

        message_off = mido.Message('note_off', note = note_to_repeat, velocity = 50, time = 300)
        track.append(message_off)

    return



def peak(track, starting_note = 0, peak_height = 11):
    """ Notes going up from the starting_note until reaching the highest_note, then going down until reaching starting_note """

    highest_note = starting_note + peak_height

    for i in range(starting_note, highest_note + 1): # Going up
        message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
        track.append(message_off)
    for i in reversed(range(starting_note, (highest_note - 1) + 1)): # Going down - It's (highest_note - 1) so that it doesn't repeat the "peak" note
        message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
        track.append(message_off)

    return



if __name__ == "__main__":
    midi_synthetic(midi_fixed_note)

    midi_synthetic(midi_repeat_aabb, up = True)
    midi_synthetic(midi_repeat_aabb, up = False)

    midi_synthetic(midi_straight_rising_octave, up = True)
    midi_synthetic(midi_straight_rising_octave, up = False)

    midi_synthetic(midi_straight_fixed_octave, up = True)
    midi_synthetic(midi_straight_fixed_octave, up = False)


    # Peaks and Valleys
    midi_synthetic(midi_peak_fixed_octave)
    midi_synthetic(midi_small_large_peaks_constant)
    midi_synthetic(midi_small_large_peaks_rising)



    # Random
    midi_synthetic(midi_random_fixed_octave)
    midi_synthetic(midi_fully_random)








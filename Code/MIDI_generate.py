""" Generating Synthetic MIDI files with specific characteristics to test our analysis """

import mido
import random


# def midi_synthetic(tempo = 361445, midi_generator, **args):
def midi_synthetic(midi_generator, tempo = 361445, **args):
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
    
    # meta2 = mido.MetaMessage('set_tempo', tempo = 361445, time = 0)
    meta2 = mido.MetaMessage('set_tempo', tempo = tempo, time = 0)
    meta_track.append(meta2)



    # Specifying the track name
    track_name_message = mido.MetaMessage("track_name", name = "Ragtime Piano")
    track.append(track_name_message)

    # Specifying the program
    program_message = mido.Message("program_change", channel = 0, program = 3, time = 0) # Piano
    # program_message = mido.Message("program_change", channel = 0, program = 40, time = 0) # Violin
    track.append(program_message)



    ### Specifying what to generate (and getting the title)
    title, note_duration, note_spacing = midi_generator(track, **args) # This is adding messages to the main track via an inputed function



    # Saving the file
    mid_path = "MIDI_files/synthetic/" + title + "_d" + str(note_duration) + "_t" + str(tempo) + ".mid"
    mid.save(mid_path)
    
    return





##################################################
#------------------------------------------------#
##################################################
# Generators

# Choose an even number of REPETITIONS (For, for example, the up down up down sequences)
REPETITIONS = 6

# Roughly the "loudness"
# VELOCITY = 50
VELOCITY = 80
NOTE_DURATION = 300 # The duration in ticks of each note
NOTE_SPACING = 20 # space between each notes




def midi_fixed_note(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, note = 1, times = REPETITIONS*12):
    """ Keeps playing the same note """
    
    repeat(track, note_duration, note_spacing, note, times)

    return "fixed_note" + "_" + str(note).zfill(3), note_duration, note_spacing # zfill pads the number to have three digits



def midi_repeat_aabb(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = 11, up = True):
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
        repeat(track, note_duration, note_spacing, i, REPETITIONS)

    if up:
        return "repeat_aabb_up", note_duration, note_spacing
    else:
        return "repeat_aabb_down", note_duration, note_spacing



#########################
## Straight Up or Down ##
#########################

def midi_straight_rising_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = (12*REPETITIONS - 1), up = True):
    """
    Do Re Mi ... - going up to different octaves
    OR
    ... Mi Re Do - going down to different octaves
    """

    straight(track, note_duration, note_spacing, starting_note, last_note, up)

    if up:
        return "straight_rising_octave_up", note_duration, note_spacing
    else:
        return "straight_rising_octave_down", note_duration, note_spacing



def midi_straight_fixed_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = 11, up = True):
    """ Do Re Mi ... Do - on a loop up at a fixed octave """

    for j in range(REPETITIONS):
        straight(track, note_duration, note_spacing, starting_note, last_note, up)
    
    if up:
        return "straight_fixed_octave_up", note_duration, note_spacing
    else:
        return "straight_fixed_octave_down", note_duration, note_spacing




#######################
## Peaks and Valleys ##
#######################

def midi_peak_fixed_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, peak_height = 11):
    """
    Straight up and down on the same octave
    Do Re Mi ... Do - on a loop down at a fixed octave
    """

    range_interval = range(REPETITIONS)

    for j in range_interval:
        peak(track, note_duration, note_spacing, starting_note, peak_height, j == range_interval[-1])

    return "peak_fixed_octave", note_duration, note_spacing



def midi_small_large_peaks_constant(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, small_peak_height = 5, large_peak_height = 11):
    """ 
    Small peak, large peak, on a loop
    """
    
    range_interval = range(REPETITIONS)

    for j in range_interval:
        peak(track, note_duration, note_spacing, starting_note, small_peak_height, last_peak = False) # Small Peak
        peak(track, note_duration, note_spacing, starting_note, large_peak_height, j == range_interval[-1]) # Large Peak

    return "peaks_small_large_constant", note_duration, note_spacing



def midi_small_large_peaks_rising(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, small_peak_height = 5, large_peak_height = 7, step = 6):
    """
    Small peak, large peak ending above (by step) the initial point
    Then loop
    Making it have a up tendency
    """

    range_interval = range(REPETITIONS)

    for j in range_interval:
        peak(track, note_duration, note_spacing, starting_note, small_peak_height) # Small Peak
        straight(track, note_duration, note_spacing, starting_note + 1, starting_note + step - 1) # Goes up by step. +1 and -1 to not replicate the notes of the peaks
        peak(track, note_duration, note_spacing, starting_note + step, large_peak_height, j == range_interval[-1]) # Large Peak ending step notes above the cycle's initial one. And only having the last note if it's the last peak of the sequence

        starting_note = starting_note + step # The next small peak starts where the large one ended

    return "peaks_small_large_rising", note_duration, note_spacing



############
## Random ##
############

random.seed(42)

def midi_random_fixed_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = 11):
    """
    Random notes within a fixed octave
    It's only on a fixed octave depending on the values of starting_note and last_note
    """
    for i in range(REPETITIONS*12):
            random_note = random.randint(starting_note, last_note) # Random number between starting_note and last_note (including)

            message_on = mido.Message('note_on', note = random_note, velocity = VELOCITY, time = note_spacing)
            track.append(message_on)

            message_off = mido.Message('note_off', note = random_note, velocity = VELOCITY, time = note_duration)
            track.append(message_off)

    return "random_fixed_octave", note_duration, note_spacing



def midi_fully_random(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING):
    """ Fully random notes """
    for i in range(REPETITIONS*12):
            random_note = random.randint(0, 127) # Random number between 0 and 127 (including)

            message_on = mido.Message('note_on', note = random_note, velocity = VELOCITY, time = note_spacing)
            track.append(message_on)

            message_off = mido.Message('note_off', note = random_note, velocity = VELOCITY, time = note_duration)
            track.append(message_off)

    return "random_fully", note_duration, note_spacing





##################################################
#------------------------------------------------#
##################################################
# Supporting Functions

def straight(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = 11, up = True):
    """ Steadily go up (or down) from starting_note until last_note """

    if up:
        range_interval = range(starting_note, last_note + 1)
    else:
        range_interval = reversed(range(starting_note, last_note + 1))

    for i in range_interval:
            message_on = mido.Message('note_on', note = i, velocity = VELOCITY, time = note_spacing)
            track.append(message_on)

            message_off = mido.Message('note_off', note = i, velocity = VELOCITY, time = note_duration)
            track.append(message_off)

    return



def repeat(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, note_to_repeat = 0, times = 1):
    """ Repeats the same note a specific number of times """

    for i in range(times):
        message_on = mido.Message('note_on', note = note_to_repeat, velocity = VELOCITY, time = note_spacing)
        track.append(message_on)

        message_off = mido.Message('note_off', note = note_to_repeat, velocity = VELOCITY, time = note_duration)
        track.append(message_off)

    return



def peak(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, peak_height = 11, last_peak = True):
    """ Notes going up from the starting_note until reaching the highest_note, then going down until reaching starting_note """

    highest_note = starting_note + peak_height

    for i in range(starting_note, highest_note + 1): # Going up
        message_on = mido.Message('note_on', note = i, velocity = VELOCITY, time = note_spacing)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = VELOCITY, time = note_duration)
        track.append(message_off)



    if last_peak: # If it's the "last peak" it'll had the final note
        down_range_interval = reversed(range(starting_note, (highest_note - 1) + 1))

    else:
    # Because there will be more peaks (or sequences) we don't want to add the final note
    # as it'll be the first of the next peak (or sequence)
        down_range_interval = reversed(range(starting_note + 1, (highest_note - 1) + 1))


    for i in down_range_interval: # Going down - It's (highest_note - 1) so that it doesn't repeat the "peak" note
        message_on = mido.Message('note_on', note = i, velocity = VELOCITY, time = note_spacing)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = VELOCITY, time = note_duration)
        track.append(message_off)

    return



if __name__ == "__main__":
    midi_synthetic(midi_fixed_note)
    midi_synthetic(midi_fixed_note, tempo = 100_000)
    midi_synthetic(midi_fixed_note, note_duration = 100)

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







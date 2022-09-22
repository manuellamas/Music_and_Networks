"""
Generating Synthetic MIDI files with specific characteristics to test our analysis
See also MIDI_add_noise.py
"""

import mido
import random
from numpy import sign

import config
from Plotting import check_dir


def midi_synthetic(midi_generator, tempo = 500_000, ticks_per_beat = 480, files_directory = "", **args):
    """ Generate a MIDI file for testing """

    # New midi file
    mid = mido.MidiFile(type = 1, ticks_per_beat = ticks_per_beat)
    """ both tempo and ticks_per_beat have as default (given as parameter to this function) the default values set as attributes when creating a MIDI file
    see all attributes on the source of mido.MidiFile() """

    meta_track = mido.MidiTrack() # Track with values and settings
    mid.tracks.append(meta_track)

    track = mido.MidiTrack() # Track with the actual notes
    mid.tracks.append(track)

    # Meta track
    meta1 = mido.MetaMessage("time_signature", numerator = 4, denominator = 4, clocks_per_click = 24, notated_32nd_notes_per_beat = 8, time = 0)
    meta_track.append(meta1)
    
    # meta2 = mido.MetaMessage('set_tempo', tempo = 361445, time = 0)
    meta2 = mido.MetaMessage('set_tempo', tempo = tempo, time = 0) # Tempo is tempo_value microseconds per beat
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
    if files_directory == "":
        mid_path = "MIDI_files/synthetic/" + title + "_d" + str(note_duration) + "_t" + str(tempo) + ".mid"
    else:
        mid_path = files_directory + "\\" + title + "_d" + str(note_duration) + "_t" + str(tempo) + ".mid"

    mid.save(mid_path)
    
    return





##################################################
#------------------------------------------------#
##################################################
# Generators

# Choose an even number of REPETITIONS (For, for example, the up down up down sequences)
REPETITIONS = 6

# Velocity is roughly the "loudness"
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

def midi_straight_rising_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = (12*REPETITIONS - 1)):
    """
    Goes straight from the starting_note to the last_note incrementing by one each time
    or decrementing if starting_note is higher than last_note
    """


    straight(track, note_duration, note_spacing, starting_note, last_note)

    if starting_note < last_note:
        return "straight_rising_octave_up", note_duration, note_spacing
    else:
        return "straight_rising_octave_down", note_duration, note_spacing



def midi_straight_fixed_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = 11, loop_times = REPETITIONS):
    """
    Goes from starting_note to last_note (up if starting_note < last_note, down otherwise)
    on a loop for loop_times number of times
    """

    for j in range(loop_times):
        straight(track, note_duration, note_spacing, starting_note, last_note)
    
    if starting_note < last_note:
        return "straight_fixed_octave_up", note_duration, note_spacing
    else:
        return "straight_fixed_octave_down", note_duration, note_spacing




#######################
## Peaks and Valleys ##
#######################

def midi_peak_fixed_octave(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, peak_height = 11, function = None):
    """
    Straight up and down on the same octave (or reverse with function = valley)
    Do Re Mi ... Do - on a loop down at a fixed octave
    """

    if function == None or function.__name__ == "peak":
        function = peak

    range_interval = range(REPETITIONS)

    for j in range_interval:
        function(track, note_duration, note_spacing, starting_note, peak_height, j == range_interval[-1])

    return function.__name__ + "_fixed_octave", note_duration, note_spacing



def midi_small_large_peaks_constant(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, small_peak_height = 5, large_peak_height = 11, function = None):
    """ 
    Small peak, large peak, on a loop (or valley with function = valley)
    """

    if function == None or function.__name__ == "peak":
        function = peak

    range_interval = range(REPETITIONS)

    for j in range_interval:
        function(track, note_duration, note_spacing, starting_note, small_peak_height, False) # Small Peak/Valley
        function(track, note_duration, note_spacing, starting_note, large_peak_height, j == range_interval[-1]) # Large Peak/Valley

    return function.__name__ + "s_small_large_constant", note_duration, note_spacing



def midi_small_large_peaks_rising(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, small_peak_height = 5, large_peak_height = 7, step = 6, function = None):
    """
    Small peak, large peak ending above (by step) the initial point
    Then loop
    Making it have a up tendency
    Or with function == valley, small valley, large valley, loop downward
    """

    if function == None or function.__name__ == "peak":
        function = peak
        tendency = "rising" # For the filename

    else:
        tendency = "falling" # For the filename
        step = -step

    range_interval = range(REPETITIONS)


    for j in range_interval:
        function(track, note_duration, note_spacing, starting_note, small_peak_height) # Small Peak/Valley
        straight(track, note_duration, note_spacing, starting_note + sign(step), starting_note + step - sign(step)) # Goes up by step. + sign(step) and - sign(step) to not replicate the notes of the peaks/valleys. And sign(step) to increment or decrement adjusting to whether it's a valley or a peak
        function(track, note_duration, note_spacing, starting_note + step, large_peak_height, j == range_interval[-1]) # Large Peak/Valley ending step notes above/bellow the cycle's initial one. And only having the last note if it's the last peak/valley of the sequence
        
        starting_note = starting_note + step # The next small peak/valley starts where the large one ended


    return function.__name__ + "s_small_large_" + tendency, note_duration, note_spacing



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



def midi_random_tendency(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, random_interval_length = 15 , random_interval_frequency = 2, random_interval_skip = 1):
    """ Random notes within an interval that's slowly growing """
    # random_interval_frequency is for how many notes will keep the same interval
    # random_interval_length is the length of the interval of numbers a note can have on a specific i
    # random_interval_skip is how much the interval's start and end values increase each time (i.e., after each random_interval_frequency has passed)



    for i in range(REPETITIONS*12):
            random_note = random.randint(i//random_interval_frequency * random_interval_skip, i//random_interval_frequency * random_interval_skip + random_interval_length - 1)
            # random_note = random.randint(0, 127) # Random number between 0 and 127 (including)

            message_on = mido.Message('note_on', note = random_note, velocity = VELOCITY, time = note_spacing)
            track.append(message_on)

            message_off = mido.Message('note_off', note = random_note, velocity = VELOCITY, time = note_duration)
            track.append(message_off)


    return "random_tendency_f" + str(random_interval_frequency) + "_l" + str(random_interval_length) + "_s" + str(random_interval_skip) , note_duration, note_spacing



#####################################
## Examples to place in the thesis ##
#####################################

def midi_mapping_example(track):
    notes_list = [
        [60, 30],
        [62, 60],
        [60, 30],
        [64, 30],
        [64, 30],
        [60, 30]
        ]

    for note, duration in notes_list:
        message_on = mido.Message('note_on', note = note, velocity = VELOCITY, time = 20)
        track.append(message_on)

        message_off = mido.Message('note_off', note = note, velocity = VELOCITY, time = duration)
        track.append(message_off)

    return "mapping_example", NOTE_DURATION, NOTE_SPACING



def midi_messages_example(track):
    notes_list = [
        [45, "on"],
        [60, "on"],
        [45, "off"],
        [45, "on"],
        [60, "off"],
        [45, "off"]
        ]

    for note, state in notes_list:
        message_on = mido.Message('note_' + state, note = note, velocity = VELOCITY, time = 20)
        track.append(message_on)

    return "messages_example", NOTE_DURATION, NOTE_SPACING



def midi_timeline_example1(track):
    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = NOTE_SPACING)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 10)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 30)
    track.append(message_off)



    return "timeline_example1", NOTE_DURATION, NOTE_SPACING



def midi_timeline_example2(track):
    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = NOTE_SPACING)
    track.append(message_on)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 10)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_off)



    return "timeline_example2", NOTE_DURATION, NOTE_SPACING



def midi_timeline_example3(track):
    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = NOTE_SPACING)
    track.append(message_on)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 30)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 10)
    track.append(message_off)



    return "timeline_example3", NOTE_DURATION, NOTE_SPACING



def midi_timeline_example4(track):
    # message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = 20)
    # track.append(message_on)

    # message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 20)
    # track.append(message_on)

    # message_on = mido.Message('note_on', note = 52, velocity = VELOCITY, time = 20)
    # track.append(message_on)

    # message_on = mido.Message('note_off', note = 52, velocity = VELOCITY, time = 20)
    # track.append(message_on)

    # message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 20)
    # track.append(message_off)

    # message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    # track.append(message_off)
    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 30)
    track.append(message_off)

    message_on = mido.Message('note_on', note = 52, velocity = VELOCITY, time = 10)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 52, velocity = VELOCITY, time = 40)
    track.append(message_off)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_off)



    return "timeline_example4", NOTE_DURATION, NOTE_SPACING



def midi_timeline_example5(track):
    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_on = mido.Message('note_on', note = 52, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_off = mido.Message('note_off', note = 52, velocity = VELOCITY, time = 20)
    track.append(message_off)



    return "timeline_example5", NOTE_DURATION, NOTE_SPACING



def midi_timeline_example6(track):
    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_on = mido.Message('note_on', note = 52, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_on = mido.Message('note_on', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 51, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_off = mido.Message('note_off', note = 52, velocity = VELOCITY, time = 20)
    track.append(message_off)

    message_on = mido.Message('note_on', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_on)

    message_off = mido.Message('note_off', note = 50, velocity = VELOCITY, time = 20)
    track.append(message_off)



    return "timeline_example6", NOTE_DURATION, NOTE_SPACING



midi_timeline_examples = [
    midi_timeline_example1
    ,midi_timeline_example2
    ,midi_timeline_example3
    ,midi_timeline_example4
    ,midi_timeline_example5
    ,midi_timeline_example6
    ]



##################################################
#------------------------------------------------#
##################################################
# Supporting Functions

def straight(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 0, last_note = 11):
    """
    Steadily go up from starting_note until last_note (including)
    Or down in case starting_note is higher than last_note
    """

    if starting_note < last_note:
        range_interval = range(starting_note, last_note + 1) # [starting_note, starting_note + 1, ..., last_note]
    else:
        range_interval = range(starting_note, last_note - 1, -1) # [starting_note, starting_note - 1, ..., last_note]

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



    if last_peak: # If it's the "last peak" it'll add the final note
        down_range_interval = range(highest_note - 1, starting_note - 1, -1) # Start one below the highest_note, and ends on the starting_note

    else:
    # Because there will be more peaks (or sequences) we don't want to add the final note
    # as it'll be the first of the next peak (or sequence)
        down_range_interval = range(highest_note - 1, starting_note, -1) # Start one below the highest_note, and ends one above the starting_note


    for i in down_range_interval: # Going down - It's (highest_note - 1) so that it doesn't repeat the "peak" note
        message_on = mido.Message('note_on', note = i, velocity = VELOCITY, time = note_spacing)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = VELOCITY, time = note_duration)
        track.append(message_off)

    return



def valley(track, note_duration = NOTE_DURATION, note_spacing = NOTE_SPACING, starting_note = 100, valley_depth = 11, last_valley = True):
    """
    Notes going down from the starting_note until reaching the lowest_note, then going up until reaching starting_note
    Essentially reverse of peak()
    """

    lowest_note = starting_note - valley_depth

    for i in range(starting_note, lowest_note - 1, -1): # Going down
        message_on = mido.Message('note_on', note = i, velocity = VELOCITY, time = note_spacing)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = VELOCITY, time = note_duration)
        track.append(message_off)



    if last_valley: # If it's the "last valley" it'll add the final note
        up_range_interval = range(lowest_note + 1, starting_note + 1) # Start one above the lowest_note, and ends on the starting_note

    else:
    # Because there will be more valleys (or sequences) we don't want to add the final note
    # as it'll be the first of the next valley (or sequence)
        up_range_interval = range(lowest_note + 1, starting_note) # Start one above the lowest_note, and ends one below the starting_note


    for i in up_range_interval: # Going down - It's (lowest_note - 1) so that it doesn't repeat the "valley" note
        message_on = mido.Message('note_on', note = i, velocity = VELOCITY, time = note_spacing)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = VELOCITY, time = note_duration)
        track.append(message_off)

    return



if __name__ == "__main__":
    main_path = config.ROOT + "\\MIDI_files\\synthetic"
    print("Creating MIDI at", main_path)
    check_dir(main_path)

    midi_synthetic(midi_fixed_note)
    # midi_synthetic(midi_fixed_note, tempo = 10_000)
    # midi_synthetic(midi_fixed_note, tempo = 300_000)
    # midi_synthetic(midi_fixed_note, note_duration = 100)
    # midi_synthetic(midi_fixed_note, note = 126)

    midi_synthetic(midi_repeat_aabb, up = True)
    midi_synthetic(midi_repeat_aabb, up = False)

    midi_synthetic(midi_straight_rising_octave, starting_note = 0, last_note = (12*REPETITIONS - 1))
    midi_synthetic(midi_straight_rising_octave, starting_note = (12*REPETITIONS - 1), last_note = 0)

    midi_synthetic(midi_straight_fixed_octave, starting_note = 0, last_note = 11)
    midi_synthetic(midi_straight_fixed_octave, starting_note = 11, last_note = 0)


    # Peaks and Valleys
    midi_synthetic(midi_peak_fixed_octave, function = peak)
    midi_synthetic(midi_peak_fixed_octave, function = valley, starting_note = 100)

    midi_synthetic(midi_small_large_peaks_constant, function = peak)
    midi_synthetic(midi_small_large_peaks_constant, function = valley, starting_note = 100)

    midi_synthetic(midi_small_large_peaks_rising, function = peak)
    midi_synthetic(midi_small_large_peaks_rising, function = valley, starting_note = 100)



    # Random
    midi_synthetic(midi_random_fixed_octave)
    midi_synthetic(midi_fully_random)
    midi_synthetic(midi_random_tendency, random_interval_length = 10 , random_interval_frequency = 3, random_interval_skip = 1)
    midi_synthetic(midi_random_tendency, random_interval_length = 15 , random_interval_frequency = 2, random_interval_skip = 1)
    midi_synthetic(midi_random_tendency, random_interval_length = 10 , random_interval_frequency = 3, random_interval_skip = 4)



    # Examples
    # To exemplify mapping
    midi_synthetic(midi_mapping_example)
    # To explain how our mapping works from the messages
    midi_synthetic(midi_messages_example)

    # To exemplify order given overlap due to mapping
    files_path = config.ROOT + "\\Dataset_Analysis\\Timeline_Bar_Test"
    print("Creating MIDI at", files_path)
    check_dir(files_path)

    for example in midi_timeline_examples:
        midi_synthetic(example, files_directory = files_path)


    # midi_synthetic(midi_timeline_example1, files_directory = files_path)
    # midi_synthetic(midi_timeline_example2, files_directory = files_path)
    # midi_synthetic(midi_timeline_example3, files_directory = files_path)
    # midi_synthetic(midi_timeline_example4, files_directory = files_path)
    # midi_synthetic(midi_timeline_example5, files_directory = files_path)



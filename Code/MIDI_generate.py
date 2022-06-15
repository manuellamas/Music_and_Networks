""" Generating Synthetic MIDI files with specific characteristics to test our analysis """

import mido


def midi_synthetic_1():
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




    ### Specifying what to generate
    # title = midi_straight_up(track)
    title = midi_repeat_up(track)




    # Saving the file
    mid_path = "MIDI_files/synthetic/" + title + ".mid"
    mid.save(mid_path)
    
    return


def midi_repeat_up(track):
    """ Repeating the same note n times until going through the entire octave """
    for i in range(0, 11+1):
        for j in range(5):
            message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
            track.append(message_on)

            message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
            track.append(message_off)


    return "repeat_up"



def midi_straight_up_rising_octave(track):
    """ Do Re Mi ... - going up to different octaves """
    for i in range(0, (12*2**5-1)+1):
        message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
        track.append(message_off)
    
    return "straight_up_rising_octave"





def midi_straight_up_rising_octave(track):
    """ Do Re Mi ... Do - on a loop up at a fixed octave """

    for j in range(5):
        for i in range(0, 11+1):
            message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
            track.append(message_on)

            message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
            track.append(message_off)
    
    return "straight_up_rising_octave"



if __name__ == "__main__":
    midi_synthetic_1()
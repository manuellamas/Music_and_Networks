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

    # # print(meta2.dict())
    # # print(meta2.type)
    # print(meta2.is_meta)




    # Specifying the track name
    track_name_message = mido.MetaMessage("track_name", name = "Ragtime Piano")
    track.append(track_name_message)

    # Specifying the program
    program_message = mido.Message("program_change", channel = 0, program = 3, time = 0)
    track.append(program_message)


    # 
    for i in range(1, 40+1):
        message_on = mido.Message('note_on', note = i, velocity = 50, time = 20)
        track.append(message_on)

        message_off = mido.Message('note_off', note = i, velocity = 50, time = 300)
        track.append(message_off)






    # Saving the file
    mid_path = "MIDI_files/synthetic/" + "straight_up" + ".mid"
    mid.save(mid_path)
    
    return




if __name__ == "__main__":
    midi_synthetic_1()
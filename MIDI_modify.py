import mido
import sys

# Original File Input
if len(sys.argv) == 1:
    print("Running sample file")
    file_path = "MIDI_files/LegendsNeverDie.mid"
else:
    file_path = sys.argv[-1]
mid = mido.MidiFile(file_path, clip = True)

def midi_program_switch(mid_file):
    # New file
    mid_adapted = mido.MidiFile()
    track = mido.MidiTrack()
    mid_adapted.tracks.append(track)

    for msg in mid_file.tracks[1]:
        if not msg.is_meta and msg.type == "program_change": # Replacing all program meta messages
            new_message = mido.Message("program_change", channel = 0, program = 127, time = 0)
            track.append(new_message)
        else: # Leaving everything else as it is
            track.append(msg)

    # original_file = "MIDI_files/created/" + original_file[0:len(mid_file.filename)-4] + "_adapted_program.mid"
    # mid_adapted.save(original_file)
    # original_file = "MIDI_files/created/" + mid_file.filename + "_adapted_program.mid"

    # ---------- SAVING THE FILE ----------
    # Getting just the file name without the path
    original_file = mid_file.filename
    start = 0
    end = len(original_file)-1
    for i , s in enumerate(original_file): # It might make more sense using Regex here

        if s == "/": # Catches the last '/'
            start = i + 1 # Exactly where the Filename starts
        elif s == ".":
            end = i # One index after the Filename ends
    original_file = original_file[start:end]

    new_file = "MIDI_files/created/" + original_file + "_adapted_program.mid"
    mid_adapted.save(new_file)

# ---------- Main ----------
if __name__ == "__main__":
    midi_program_switch(mid)
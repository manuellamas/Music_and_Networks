# Change a MIDI file
# With program change, create a new version of a midi file and change it for for example 127
# Remember that a track is a list

import mido

  Message('program_change', channel=0, program=127, time=0),
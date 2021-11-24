Took a [midi file sample from wikipedia](https://en.wikipedia.org/wiki/File:MIDI_sample.mid?qsrc=3044).

### Documenting how I'm doing it
The graph is being created by looking only at each note's start. Meaning *I'm currently ignoring the velocity and duration*.
A note x comes after another note y if it's start comes immediately after it. If that happens there will be a directed link from note x -> y.

- Analyze all instruments at once? Or track by track (only one track for now)?
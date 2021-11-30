import mido
import Graph

command = ""
file_path = input("Enter MIDI File:\n")

while command != "quit":
    # command_list = command.split() # Splits by whitespace(s)
    if command == "change file":
        file_path = input("Enter MIDI File:\n")
    elif command == "graph":
        mid_file = mido.MidiFile(file_path, clip = True)
        notes = Graph.get_notes(mid_file)
        graph = Graph.create_graph_from_notes(notes)
        print("Variable 'graph' now holds the graph of the corresponding 'file_path'")

    command = input("Insert new command")

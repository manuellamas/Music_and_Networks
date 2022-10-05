For the overlap examples, that reside in this folder.

fontsize = 14 on both x and y labels
and tick labelsize = 14



    ax.set_xlabel('Ticks', labelpad = 9, fontsize = 14) # labelpad padding between the label and the ticks
    ax.set_ylabel('MIDI note codes', labelpad = 6, fontsize = 14)

    # Ticks Text Size
    ax.tick_params(axis='both', which='major', labelsize = 14)
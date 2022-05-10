"""
Example program to show how to read a multi-channel time series from LSL.

hot to test: open any LSL compatible recording application, line openBCI or audiocapture

"""

from pylsl import StreamInlet, resolve_stream, resolve_byprop

"""
TESTING
comment the following section if you don't need it
"""
# RANDOM TESTING
def testing():
    """
    here I'm just playing around
    """

    def print_outlets(streams):
        if len(streams)==0: print("no outlet found"); return 1
        print("names of available outlets:")
        for s in streams:
            print ("\t-> "+s.name())
        return 0
    # using resolve_stream without any arguments
        # runs resolve_streams() without arguments: looks for ALL outlets
    streams = resolve_stream()
    print_outlets(streams)

    # using resolve_streams with first argument string, second argument string
        # this runs resolve_by_prop with the two string arguments
        # NOTE: timeout is forever by default, and you can't change it from here! QUESTION: how to?
    streams = resolve_stream('type', 'EEG') 
    print(streams)

    # find streams using resolve_byprop directly
    streams = resolve_byprop( prop= "type", value= "EEG", timeout=1)
    print_outlets(streams) 

    # find streams using resolve_byprop directly, 
    # using audiocapture lsl output, with a specific name
    streams = resolve_byprop( prop= "name", value= "MyAudioStream", timeout=1)
    print_outlets(streams) 

    # create a new inlet to read from the stream
    inlet = StreamInlet(info= streams[0], max_buflen=360, max_chunklen=0, recover=True)

    sample, timestamp = inlet.pull_sample()

"""
defining some useful functions
"""

def print_streams_info(streams):
    for i in range(len(streams)):
        print(  "outlet {}"             .format(i)                                  )
        print(  "\tname:\t\t{}"         .format(streams[i].name())                  )
        print(  "\ttype:\t\t{}"         .format(streams[i].type())                  ) 
        print(  "\t#_channels:\t{}"     .format(streams[i].channel_count())         )
        print(  "\ts_rate:\t\t{}"       .format(streams[i].nominal_srate())         )
        print(  "\tdtype:\t\t{}"        .format(streams[i].channel_format())        )
        print(  "\tID:\t\t{}"           .format(streams[i].source_id())                                                )

def find_available_streams(return_all=True):
    # search for all outlets
    print("finding available outlets...\n")
    streams = resolve_stream()
    print_streams_info(streams)

    if return_all==True:
        print("all streams selected")
        return streams 

    else: 
        selection = select_stream(streams)
        new_list = []
        # return only selected elements
        for i in range(len(selection)):
            new_list.append( streams[i] )
        return new_list

def select_stream(streams):
    """..."""
    stream_list = []
    while True:
        choice = int(input("select positive number, or -1 if you're done"))
        if choice == -1:
            break 
        else: stream_list.append(streams[choice])
    return stream_list 

streams = find_available_streams(return_all=False)

print("selected streams: ")
print_streams_info(streams)





def main():
    # first resolve (find) an EEG stream on the lab network
    print("looking for an EEG stream...")
    # create a list of streams?
    streams = resolve_stream('type', 'EEG') # don't I need any other specifiers?
    
    # create a new inlet to read from the stream
    inlet = StreamInlet(info= streams[0])

    while True:
        # get a new sample (you can also omit the timestamp part if you're not interested in it)
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)


if __name__ == '__main__':
    main()





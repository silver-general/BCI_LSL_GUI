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





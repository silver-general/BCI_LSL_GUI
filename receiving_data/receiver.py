from pylsl import StreamInlet, resolve_stream, resolve_byprop, local_clock


"""
helper functions from receiving data functions
"""
def print_streams_info(streams):
    """
    prints the StreamInfo information of a list of outlets
    """
    for i in range(len(streams)):
        print(  "outlet {}"             .format(i)                                  )
        print(  "\tname:\t\t{}"         .format(streams[i].name())                  )
        print(  "\ttype:\t\t{}"         .format(streams[i].type())                  ) 
        print(  "\t#_channels:\t{}"     .format(streams[i].channel_count())         )
        print(  "\ts_rate:\t\t{}"       .format(streams[i].nominal_srate())         )
        print(  "\tdtype:\t\t{}"        .format(streams[i].channel_format())        )
        print(  "\tID:\t\t{}"           .format(streams[i].source_id())             )

def find_available_streams(return_all=True):
    """
    finds all streams. 
    INPUT
        return_all: true of you want to find all, otherwhise you can select them
    """
    # search for all outlets
    print("finding available outlets...\n")
    streams = resolve_stream()
    print_streams_info(streams)

    if len(streams)==0:
        print("no outlets found!")
        return None

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
    """selects only one!"""
    stream_list = []
    while True:
        choice = int(input("select positive number, or -1 if you're done"))
        if choice == -1:
            break 
        else: 
            stream_list.append(streams[choice])
            break
    return stream_list 


"""
function that plots samples

use spammer.py to send some values
"""

def receiver(stream,T):
    """
    received data for a while
    INPUT
        stream: stramInfo object
        T: time to receive
    """

    data = []

    # create inlet
    inlet = StreamInlet(info=stream, max_buflen=360, max_chunklen=0, recover=True)

    sample_number = 0

    # open streaming session. data will be buffered I guess? so this is probably why I get more samples!
    #inlet.open_stream()

    # define start time
    start_time = local_clock()

    while True:
        
        if local_clock()-start_time > T:
            break
        
        # timeout forever means it will wait until a sample is available!
        sample = inlet.pull_sample(timeout=100, sample=None)
        
        #print(sample)
        data.append(sample)
        sample_number += 1



    inlet.close_stream()
    elapsed = local_clock() - start_time

    print("sampling rate of outlet: {} Hz".format( inlet.info().nominal_srate() ))
    print("samples received: {}".format(sample_number) )
    print("elapsed time: {}".format(elapsed))

    return data

# find and select stream
streams = find_available_streams()
info = streams[int(input("select stream number"))]

data = receiver(info,2)

"""
QUESTION: WHY DO I GET ONE SAMPLE MORE? 
"""
for i in data:
    print(i)
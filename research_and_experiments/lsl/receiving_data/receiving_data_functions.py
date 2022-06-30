from pylsl import StreamInlet, resolve_stream, resolve_byprop, local_clock

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
    """select only one!"""
    stream_list = []
    while True:
        choice = int(input("select positive number, or -1 if you're done"))
        if choice == -1:
            break 
        else: 
            stream_list.append(streams[choice])
            break
    return stream_list 

# try that
streams = find_available_streams(return_all=True)

print("selected streams: ")
print_streams_info(streams)



"""
creating an inlet object
"""

inlet = StreamInlet(info= streams[0], max_buflen=360, max_chunklen=0, recover=True)





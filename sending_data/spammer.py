"""
this file is used to create a sender with simple parameters to debug receivers
"""

import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock


def main(argv):
    
    # define default parameters for the outlet StreamInfo data
    srate = 5 
    name = 'spam_stream'
    type = 'spam'
    n_channels = 1

    # define the error message sent if arguments are not valid
    help_string = 'spammer.py -s <sampling_rate> -n <stream_name> -t <stream_type>'
    try:
        # NOTE: you can also run the program with default arguments!
        opts, args = getopt.getopt(argv, "hs:c:n:t:", longopts=["srate=", "channels=", "name=", "type"])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts: 
        # opts is an iterable.
        #   opt is the i-th option. can be short or long, eg: -s or --srate
        #   arg is the argument passed
        if opt == '-h': # in case user asked for help!
            print(help_string)
            sys.exit()
        elif opt in ("-s", "--srate"):
            srate = float(arg)
        elif opt in ("-c", "--channels"):
            n_channels = int(arg)
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-t", "--type"):
            type = arg

    # create info for your stream
    info = StreamInfo(name= name, type= type, channel_count= n_channels, nominal_srate= srate, channel_format= 'float32', source_id= 'myuid34234')

    # create an outlet
    # creating an outlet object
    outlet = StreamOutlet(info)
    print("stream info:")
    print("name: {}\ntype: {}\nn_channels: {}\nsrate: {}Hz\ndtype: {}\nID: {}\n".format(info.name(),info.type(),info.channel_count(),info.nominal_srate(),info.channel_format(),info.source_id()))
    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0

    while True:

        elapsed_time = local_clock() - start_time
        
        required_samples = int(srate * elapsed_time) - sent_samples
            
        # create samples for each channel and push
        # values here are increasing 0 to 10 and repeating, same for all channels
        for sample_ix in range(required_samples):

            mysample = [(local_clock() - start_time)%10 for _ in range(n_channels)]            
            
            outlet.push_sample(mysample)


        sent_samples += required_samples

        time.sleep(0.05)



if __name__ == "__main__":
    main(None)
















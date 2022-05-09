"""
Example program to demonstrate how to send a multi-channel time series to LSL.
from: https://github.com/labstreaminglayer/liblsl-Python/blob/master/pylsl/examples/SendData.py

TO TRY THIS PROGRAM
use any recording program like Labrecorder and find the outlet into the stream list. record an XML file and check metadata
"""
import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock


def main(argv):
    srate = 100 # sampling rate?
    name = 'BioSemi'
    type = 'EEG'
    n_channels = 4
    # help_string is the error message sent if arguments are not valid
    help_string = 'SendData.py -s <sampling_rate> -n <stream_name> -t <stream_type>'
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
    """
    CREATING A NEW STREAM INFO

    first create a new stream info
        name to BioSemi
        the content-type to EEG
        8 channels
        sampling at 100 Hz
        float-valued data 
        serial number of the device: or some other more or less locally unique identifier for the stream as far as available 
            you could also omit it but interrupted connections wouldn't auto-recover)
    """
    info = StreamInfo(name= name, type= type, channel_count= n_channels, nominal_srate= srate, channel_format= 'float32', source_id= 'myuid34234')
    
    # creating an outlet object
    outlet = StreamOutlet(info)
    print("stream info:")
    print("name: {}\ntype: {}\nn_channels: {}\nsrate: {}Hz\ndtype: {}\nID: {}\n".format(info.name(),info.type(),info.channel_count(),info.nominal_srate(),info.channel_format(),info.source_id()))
    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0
    while True:

       # update elapsed time. how much time has passed since the start of the program?
        elapsed_time = local_clock() - start_time
        
        # this is how you decide the number of samples needed depending on the time elapsed.
        # is this because in streaming data sometimes you're in time, sometimes you're late and you need more samples???
        required_samples = int(srate * elapsed_time) - sent_samples
            # srate*elapsed_time is the number of samples that SHOULD HAVE BEEN sent in the elapsed time
            # you take away the samples that you already sent to get the ones you need to send.
            # each sample is a list of n_channels elements, one for each channel
        
        # for each of the required samples
        for sample_ix in range(required_samples):
            
            # make a random new sample of n_channels elements; 
            # this is converted into a pylsl.vectorf (the data type that is expected by push_sample)
            mysample = [rand() for _ in range(n_channels)]            
            
            # now send it
            outlet.push_sample(mysample)

        # update how many samples were sent. this will be used to compute how many samples are needed to be streamed
        # they also depend on elapsed time!
        sent_samples += required_samples
        # now send it and wait for a bit before trying again.
        time.sleep(0.01)


if __name__ == '__main__':
    #main(sys.argv[1:])
    main(None) # if you want to play it in the itneractive window with default arguments

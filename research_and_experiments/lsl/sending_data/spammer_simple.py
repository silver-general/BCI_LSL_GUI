"""
this file is used to create a sender with simple parameters to debug receivers
"""

import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock


def main():
    
    # define default parameters for the outlet StreamInfo data
    srate = 10 
    name = 'spam_stream'
    type = 'spam'
    n_channels = 1


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

            # if you want to send a sample whose value is a range of numbers: 0,..,10,0,..,10,..
            mysample = [(local_clock() - start_time)%10 for _ in range(n_channels)]            
            
            outlet.push_sample(mysample)


        sent_samples += required_samples

        time.sleep(0.05)



if __name__ == "__main__":
    main()
















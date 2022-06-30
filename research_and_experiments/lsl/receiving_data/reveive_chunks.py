"""Example program to demonstrate how to read a multi-channel time-series
from LSL in a chunk-by-chunk manner (which is more efficient)."""

from pylsl import StreamInlet, resolve_stream
import time

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream()

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    chunks = []
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        chunks.append (inlet.pull_chunk(timeout=1) )
        chunks.append (inlet.pull_chunk(timeout=1) )
        break

type(chunks)
len(chunks)

type(chunks[0]) # first chunk

type(chunks[0][0]) # list of chunks of first chunk
len(chunks[0][0]) # N chunks, each is a list of 16 channels

##########
type(chunks[0][0][0]) # first sample 
len(chunks[0][0][0])

type(chunks[0][1]) # list of timestamps of first chunk
len(chunks[0][1]) # N timestamps, one for each sample
type(chunks[0][1][0]) # first timestamp

##########
type(chunks[0][0][1]) # second sample 
len(chunks[0][0][1])

type(chunks[0][1][1]) # second timestamp



samples = []
samples.append( (chunks[0][0][0], chunks[0][1][0]) ) # append a sample and its timestamp
print(samples)

samples = []

# for each chunk
for j in range(len(chunks)): # iterate over chunks: chunks[j]
    # for each sample in the chunk
    for i in range(len( chunks[j][0] )):

        sample = chunks[j][0][i]
        timestamp = chunks[j][1][i]

        #print( "\ntimestamp:", timestamp,"\nsample:",sample )
        #print( tuple((timestamp,sample)) )
        samples.append( tuple((timestamp, sample)) )
        #break
    #break 
print(samples[0]) # first "timestamp, sample"
print(samples[1])
print(samples)


if __name__ == '__main__':
    main()
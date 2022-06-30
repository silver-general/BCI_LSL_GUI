"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream, local_clock


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream()

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    duration = 1 # in seconds

    samples = []

    start = local_clock()
    while local_clock()-start <= duration:
        
        samples.append( inlet.pull_sample() )
        #print(local_clock()-start)
    
    elapsed = local_clock()-start
    print("elapsed time: ",str(elapsed))
    print("samples that were taken: {}".format(len(samples)))
    print("samples that should've been taken: {}".format( elapsed * inlet.info().nominal_srate() ) )

if __name__ == '__main__':
    main()
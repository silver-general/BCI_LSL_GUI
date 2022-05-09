"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream


def main():
    # first resolve (find) an EEG stream on the lab network
    print("looking for an EEG stream...")
    # create a list of streams?
    streams = resolve_stream('type', 'EEG',wait_time=1.0) # don't I need any other specifiers?
    streams = resolve_stream()
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    while True:
        # get a new sample (you can also omit the timestamp part if you're not interested in it)
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)


if __name__ == '__main__':
    main()





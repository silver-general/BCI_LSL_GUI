"""
"""

from pylsl import StreamInlet, resolve_stream, resolve_byprop, local_clock, StreamInfo


info = StreamInfo("MetaTester", "EEG", 8, 100, "float32", "myuid56872")


# get info back
print(info.as_xml())    


def main():

    outlet = find_stream()

    
    metadata = {"Patient Data" : {}, "Experiment Type" : {} }


    outlet = setup_metadata(outlet)

    show_XML(outlet)

    inlet = StreamInlet(outlet)
    
    samples = record(inlet, duration = 2)

    show_results(samples)


def find_stream():
    print("looking for an EEG stream...")
    streams = resolve_stream() 

    text = ""
    if len(streams)==0:
        text = "No soutlets found!"
        print("available streams: " + text)
    else:
        print("available streams:")
        for outlet in streams:
            text = "\toutlet index: {}\n\t\tname:\t\t{}\n\t\ttype:\t\t{}\n\t\tchannels\t\t{}\n\t\tsrate\t\t{}\n\t\tformat\t\t{}\n\t\tsource id\t{}".format(streams.index(outlet),outlet.name() , outlet.type() , outlet.channel_count(), outlet.nominal_srate(), outlet.channel_format(), outlet.source_id())
            print(text)
    
    i = int(input("select stream index: "))
    return streams[i]

def record(inlet, duration = 0):
    
    samples = []

    print(f"recording duration: {duration}")
    
    start = local_clock()
    print( f"recording starts at: {start}")
    
    while ( local_clock() - start <= duration ):
        print( local_clock() - start )
        #samples.append( inlet.pull_sample() )
    
    elapsed = local_clock()-start

    print("recording complete. elapsed time: {}".format(elapsed))
    #print("samples that were supposed to be recorded: {}".format( duration*inlet.info().nominal_srate() ))
    print("samples actually recorded: {}".format( len(samples) ))

    return samples

def show_results(samples):
    pass

def setup_metadata(info):

    """
    HOW TO STORE METADATA BEFORE PASSING IT TO THE STREAMINFO OBJECT?
    I want to build some sort of dictionary
    for example, how to model
        patient data
            name: ...
            surname: ...
            age: ...
        experiemnt
            type: ...
            duration: ...
    """

    # handle metadata here. 
    # NOTE: .desc() is a section of the XML metadata!


    # dummy metadata
    info = StreamInfo("MetaTester", "EEG", 8, 100, "float32", "myuid56872")

    patient_data = { "Name": "Alberto", "Surname":"Morgana","Age":"29" }
    experiment_data = {"Type" : "Receiving from spammer.py and saving in XML", "Duration":"Not specified"}
    data = { "Patient Data" : patient_data, "Experiment Data": experiment_data}

    # extracting data from the dictionary
    for child in data.keys():

        print(child)
        handle = info.desc().append_child(child)
        

        for key in data[child].keys():
            print("\t"+key)
            print("\t\t"+ data[child][key])
            handle.append_child_value(key, data[child][key])

    print(info.as_xml())

    patient_data = info.desc().append_child("Patient Data")
    patient_data.append_child_value("Name", "Alberto")
    patient_data.append_child_value("Surname", "Morgana")
    patient_data.append_child_value("Age","29")

    experiment_data =  info.desc().append_child("Experiment Data")
    experiment_data.append_child_value("Type", "Simple streaming experiment using a spammer.py")

    return info

def show_XML(info):
    print(info.as_xml())


if __name__ == '__main__':
    main()
    print("main function completed")

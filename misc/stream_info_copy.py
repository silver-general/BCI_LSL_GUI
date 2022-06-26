from pylsl import StreamInfo



info = StreamInfo()
print(info.as_xml())

experiment_info = info.desc().append_child("Experiment Info")
experiment_info.append_child_value("Type", "Motor Imagery")

print(info.as_xml())

experiment_info = info.desc().append_child("Experiment Info") # this one substitutes the previous child
experiment_info.append_child_value("Type", "Motor Imagery")
experiment_info.append_child_value("Type", "Motor Imagery")

type(info)
type(info.desc())
type(experiment_info)

info.desc().remove_child ( info.desc().child_value("Experiment Info") )
print(info.as_xml())



type(info.desc().child("Experiment Info"))
print( info.desc().child("Experiment Info") )

info.desc().remove_child( info.desc().child("Experiment Info") )





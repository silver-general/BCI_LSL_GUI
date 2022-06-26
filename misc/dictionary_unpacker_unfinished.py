"""
given a dictionary of dictionaries, it unpacks it into text
"""

dict_1 = { "element1" : 11, "element2":12,"element3":13 }
dict_2 = { "element1" : 21, "element2":22,"element3":13, "element4":dict_1 }

dict_3 = { "element1" : 31, "element2": dict_2 , "element3":33 }




def unpacker(dictionary, text = "", indent = 0):

    stop = True

    # base case: no dictionary in dictionary
    for key in dictionary.keys():
        if type(dictionary[key] == dict):
            stop = False
            break

    if stop == True:
        text = text + "key:\t{}\nvalue:\t{}".format(key, dictionary[key])


            

    

    for key in dictionary.keys():
        text = text + "key:\t{}\nvalue:\t{}".format(key, dictionary[key])
        print()

unpacker(dict_3, text = "")



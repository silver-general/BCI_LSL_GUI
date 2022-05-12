import getopt
import sys 

"""
batch commands

note how the next command calls the same argument "-s" twice and as results it overwrites the first!
note how the argument "-spam" gets understood as "-s pam"
    dates.py -s 16-04-1993 -e 01-01-2020 -spam "spam spam spam" -s "spam"

dates.py -s 16-04-1993 -e 01-01-2020 "spam spam spam" -s "spam"

the following does miss a value for an argument
    dates.py -s 16-04-1993 -e 

CORRECT ONES

dates.py -s 16-04-1993 -e 01-01-2020 
    this one uses short options
dates.py --start_date 16-04-1993 --end_date 01-01-2020 
    this uses long options

"""

def parse_0():

    start_date = None
    end_date = None 

    argv = sys.argv
    print("command line arguments passed:\n{}\n".format(argv))

    argv = argv[1:]
    print("deleted filename. command line list now is:\n{}\n".format(argv))

    """
    parsing the list of arguments
    you need exactly to pass -s -e and their values, not different arguments!
    opts will be a list of tuples, the parsed arguments!
    args will be a list of arguments that have not been processed!
    the columns after the arguments mean that they require a value!
    note: any additional argument might be confused with the previous!
    EG what happens if you run 
        dates.py -s 16-04-1993 -e 01-01-2020 -spam "spam spam spam" -s "spam"
        -> the parsed arguments will have the second -s overwriting the first!
        solution: do not pass the same argument twice!
    """
    opts, args = getopt.getopt(argv, shortopts = "s:e:")

    print("arguments parsed:\n{}\n".format( opts ))
    print("arguments not parsed:\n{}\n".format( args ))

    """
    iterate over options and arguments to extract data
    """
    for opt, arg in opts:
        # opt: option
        # arg: value
        if opt in ["-s"]:
            start_date = arg 
        elif opt in ["-e"]:
            end_date = arg 
    

    print("start date:\t\t{}\nend date:\t\t{}\n".format(start_date,end_date))

    return 0



def parse_1():
    """
    this one handles exceptions and uses long arguments
    """

    start_date = None
    end_date = None 

    argv = sys.argv
    print("command line arguments passed:\n{}\n".format(argv))

    argv = argv[1:]
    print("deleted filename. command line list now is:\n{}\n".format(argv))


    # parsing the list of arguments
    try:
        opts, args = getopt.getopt(argv, shortopts = "s:e:", longopts= ["start_date=","end_date="])
    except getopt.GetoptError as error:
        print(error)
        # set opts to an empty list
        opts = []

    print("arguments parsed:\n{}\n".format( opts ))
    print("arguments not parsed:\n{}\n".format( args ))

    
    # iterate over options and arguments to extract data
    for opt, arg in opts:
        # opt: option
        # arg: value
        if opt in ["-s", "--start_date"]:
            start_date = arg 
        elif opt in ["-e","--end_date"]:
            end_date = arg 
    
    print("start date:\t\t{}\nend date:\t\t{}\n".format(start_date,end_date))

    return 0


# run functions
parse_1()

# terminating message, stops executions
input("program terminated. press anything to exit: ")


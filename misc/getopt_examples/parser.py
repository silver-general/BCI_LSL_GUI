import getopt, sys 

"""
different command line options

parser.py -s 16-04-1993 -e 01-01-2020 
    correct one

parser.py -s 16-04-1993 -e 01-01-2020 -spam "spam spam spam" -p "spam"
    this one parses one additional ("-s", "pam")
parser.py -s 16-04-1993 -e 01-01-2020  -spam 
parser.py -s 16-04-1993 -e 01-01-2020 -spam "spam spam spam" 
parser.py -s 16-04-1993 -e 01-01-2020 -spam "spam spam spam" -p "spam"

parser.py -s 16-04-1993 -e 01-01-2020 -spam  -p "spam"
    why does this crashes? QUESTION

"""

def main():

    start_date = None 
    end_date = None

    # all arguments
    argv = sys.argv
    print("command line arguments:\n{}\n".format(argv))

    # remove filename for parsing
    argv = argv[1:]
    print("command line arguments, no filename:\n{}\n".format(argv))

    # parsing
    try:
        opts, args = getopt.getopt(argv, shortopts= "s:e:")
    except: 
        print( getopt.GetoptError )
    print("parsed arguments:\n{}\n".format(opts))
    print("non-parsed arguments:\n{}\n".format(args))
    
    for opt,arg in opts:
        if opt in ["-s"]:
            start_date = arg
        if opt in ["-e"]:
            end_date = arg
    print("start date:\t\t{}\nend date:\t\t{}\n".format(start_date,end_date))

    return 0


if __name__ == "__main__":

    main()
    input("press anything to exit: ")


try:
    print(asd)
except NameError:
    print("an error has occurred")
except:
    print("unknown error")
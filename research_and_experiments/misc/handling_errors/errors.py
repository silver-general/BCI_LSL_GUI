"""
https://www.w3schools.com/python/python_try_except.asp

"""
import sys, getopt

def f1():
    print("trying to print a thing")
    try:
        print(s)
    except NameError:
        print("error: variable was not defined!")
    except:
        print("unknown error")
    finally:
        print("failed printing")

    """ quickly write a bunch of things on a file """
    print("trying to write to a file")
    try:
        file = open("file.txt", mode="w")
        file.write("hello, brave new world!")
    finally:
        file.close()


""" try to write when it's just reading mode """
def f2():
    print("trying to write on a file")
    try: 
        file = open("file.txt", mode="r")
        file.write("hello, brave new world!")
    except:
        print("an error occurred while writing! ")
    finally:
        print("finished trying to write something.")


""" raising exceptions """

"""
command line
(CORRECT) errors.py -a 32
"""
def f3():
    """ get a number from command line and print it. if not a number, raise exception """
    number = None
    
    argv = sys.argv[1:]

    try:
        print("trying to parse command line arguments")
        input("press any")
        opts, args = getopt.getopt(argv, shortopts="a:")
    except: 
        print("error parsing arguments!")
        input("press anything to continue")
    print("parsed arguments: \n{}".format( opts ) )
    input("press any")

    for opt,arg in opts:
        if opt in ["-a"]:
            number = arg
    
    input("now checking type of number. press anything")
    
    
    if type(number) != int:
        raise TypeError("only ints allowed!")
    
    print("number chosen: {}".format(number))



if __name__=="__main__":

    print("comamnd line arguments (excluding filename):\n {}".format(sys.argv[1:]))
    input("press anything to continue")
    f3()
    input("\nprogram terminated.")

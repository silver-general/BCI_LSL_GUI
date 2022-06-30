import sys
import getopt
  

def full_name():
 
    # defaults
    first_name = None
    last_name = None
  
    # take all command line arguments except the file name
    argv = sys.argv[1:]
  
    # try to parse command lines 
    try:
        opts, args = getopt.getopt(argv, shortopts= "f:l:", longopts= [ "first name =","last_name =" ])
      
    except:
        print("error")
  
    for opt, arg in opts:
        if opt in ['-f',"--first_name"]:
            first_name = arg
        elif opt in ['-l',"--last_name"]:
            last_name = arg
      
  
    print( first_name +" " + last_name)
  
    x = input("type anything to exit: ")

full_name()  
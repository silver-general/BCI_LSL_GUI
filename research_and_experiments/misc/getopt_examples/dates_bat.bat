@ECHO OFF

REM note how the next command calls the same argument "-s" twice and as results it overwrites the first!
REM note how the argument "-spam" gets understood as "-s pam"
REM dates.py -s 16-04-1993 -e 01-01-2020 -spam "spam spam spam" -s "spam"

REM rem dates.py -s 16-04-1993 -e 01-01-2020 "spam spam spam" -s "spam"

REM the following does miss a value for an argument
REM dates.py -s 16-04-1993 -e 

REM this uses long options
dates.py --start_date 16-04-1993 --end_date 01-01-2020 

PAUSE
import subprocess
import sys
import os
import argparse
import datetime
import re

#################################
# Kyle Quinn
# CSCI 356 Networks
# Project 0: Due 2/2/17
# KyleQuinn_P0.py
#################################


def execute(dst, idx):
    subprocess.call(dst[int(idx)])
    print("Done.\n")


def display(st):
    flag = True
    while flag:
        try:
            idx = int(raw_input("Please Enter the Integer Index of the File To Execute. (e.g. 1): "))
        except ValueError:
            print("Error! Non-numeric Input.")
        else:
            if int(idx) not in range(1, len(st)):
                print("Please Try Again - Index Not In Acceptable Range!\n")
            else:
                flag = False
    return idx


def index_file(fileA):
    max_count = 10  # FIX: For Future Use: All Results, Not Limited to 10
    a = [None] * max_count
    index = 0
    with open(fileA) as fA:
        for line in fA:  # Assumes Multiple Lines Can Be Written. Precaution.
            b = line.split()
            for item in b:
                if len(b) == 1:
                    print("Executable: %s Does Not Exist!\n") % item
                    print("Please Enter The Name of an Executable.\n")
                    return b
                else:
                    if index == 0:
                        print("***** %s *****") % item
                    else:
                        print"Item Index %s = %s" % (index, item)
                    a[index] = item
                    index += 1
        return a


def launch(*argv):
    fn = unicode(datetime.datetime.now())
    fn = (re.sub(r'[^\w]', ' ', fn) + ".txt").replace(" ", "")
    f = open(fn, "w")
    try:
        if os.stat(fn).st_size == 0:
            subprocess.call(argv, stdout=f)
            b = index_file(fn)
            if len(b) > 1:
                c = display(b)
                if isinstance(c, int):
                    execute(b, c)
                else:
                    print "Cannot Write to File %s: Contains Information" % fn
    except OSError:
        print "File Does Not Exist OR Permission Denied"
    f.close()
    os.remove(fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter Name of Executable <Pattern>.')
    parser.add_argument('Pattern', type=str, help='Name of Executable; (e.g. firefox)')
    args = parser.parse_args()
    launch("whereis", args.Pattern)

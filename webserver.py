import os
import sys
import socket
import time
import re
import random
import threading
import argparse


def timestamp():
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())


def gen_random():
    return random.randint(1, 100)  # Integer from 1 to 100, endpoints included


def http_response(st_in):  # fix static vs dynamic vs page not found
    time_stamp = timestamp()
    rand = gen_random()
    print"Data Captured: ", st_in

    header = '''HTTP/1.1 200 OK
Date: %s
Server: 4b4a51-%d_Server
Last-Modified: Sun, 14 Feb 2010 21:57:18 GMT (fix)
Content-Length: 57 (fix)
Connection: close
Content-Type: text/plain
Edit - The time is now %s. Bye!''' % (time_stamp, rand, time_stamp)

    return header


def check_content_type(header):
    pattern = re.compile("hello (.*?)\n")
    content_type = pattern.search(str(header))  # Dynamic Keyword Search: "hello"
    return content_type


def dynamic_response():
    rand = gen_random()
    response = "Generic Dyanmic Response - %d\n" % rand
    return response


def file_check(directory, fileA):
    filename = str(directory) + str(fileA)
    print filename
    try:
        open(filename, "r")
    except IOError:
        print "Error: File Does Not Exist"
    else:
        return filename


def parse_request(header):
    split_header = []
    pattern = re.compile("GET (.*?)\n")
    parse_header = pattern.match(header)  # return a corresponding MatchObject. Return None if the string != pattern

    if parse_header is not None:
        split_header = re.split("\s+", header)

    return parse_header, split_header


#########################################
# Kyle Quinn
# CSCI 356 Networks
# Project 1: Checkpoint 9pm Tuesday 2/14
# Last Modified: 2/7/17 11:19pm
#########################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Basic web server, in python.')
    parser.add_argument('Port_Number', type=int, help='Your server should listen for connections on specified port.')
    parser.add_argument('Directory_Name', type=str, help='Directory name for the document root.')
    args = parser.parse_args()

    HOST = socket.gethostname()
    PORT = args.Port_Number
    DIR = args.Directory_Name

    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # A pair (host, port) is used for the AF_INET address family\
    #  SOCK_STREAM constants represent the socket types
    s.bind((HOST, PORT))
    s.listen(1)  # Listen for connections made to the socket. The backlog argument specifies MAX# queued connections
    print"Listening on PORT %d\n" % PORT  # Error Checking
    conn, addr = s.accept()  # Accept a connection. The socket must be bound to an address and listening for connections
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)  # Receive data from the socket. The return value is a string representing the data\
        #  received. The maximum amount of data to be received at once is specified by bufsize
        if not data:
            break
        else:
            request, fn = parse_request(data)  # Read from that new socket, parse the HTTP request.
            print("Parsing Request.\n")
            if request:
                dynamic_content = check_content_type(request)
                if dynamic_content:
                    send = dynamic_response()
                    conn.sendall(send)  # Send data to the socket. The socket must be connected to a remote socket.
                    print"Sent response, content length was %d\n" % (len(send))
                else:
                    parsed_file = file_check(DIR, fn[1])
                    if parsed_file:
                        send = 'Sent File ... Placeholder'
                        conn.sendall(send)  # Send data to the socket. The socket must be connected to a remote socket.
                        print"Sent response, content length was %d\n" % (len(send))
                    else:
                        print("Error 404! Invalid? \n")
            else:
                print("This request is Not a GET Request!\n")
                # TODO Extra Credit Goes Here!
                break
    conn.close()
    print"Connection Closed.\n"


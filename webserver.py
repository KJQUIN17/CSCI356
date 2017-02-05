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


def http_response():  # fix static vs dynamic vs page not found
    time_stamp = timestamp()
    rand = gen_random()

    header = '''HTTP/1.1 200 OK
Date: %s
Server: 4b4a51-%d_Server
Last-Modified: Sun, 14 Feb 2010 21:57:18 GMT (fix)
Content-Length: 57 (fix)
Connection: close
Content-Type: text/plain

The time is now %s. Bye!'''
    return header % (time_stamp, rand, time_stamp)


def parse_request(header):
    pattern = re.compile("GET (.*?)\n")
    parse_header = pattern.match(header)  # return a corresponding MatchObject. Return None if the string != pattern

    # TODO: Potentially use re.split(pattern, string, maxsplit=0, flags=0) to return string
    return parse_header


#########################################
# Kyle Quinn
# CSCI 356 Networks
# Project 1: Checkpoint 9pm Tuesday 2/14
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
    conn, addr = s.accept()  # Accept a connection. The socket must be bound to an address and listening for connections
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)  # Receive data from the socket. The return value is a string representing the data\
        #  received. The maximum amount of data to be received at once is specified by bufsize
        if not data:
            break
        else:
            request = parse_request(data)  # Read from that new socket, parse the HTTP request.
            if request is not None:
                # Request is a GET request
                send = http_response()
                conn.sendall(send)  # Send data to the socket. The socket must be connected to a remote socket. \
            else:
                print("Static case, just print an error message and quit!\n")
                fn_path = str(DIR) + str(send)  # TODO  - be able to open this file in firefox
                print fn_path

#                 Fix case 2.d above by adding code to handle static content:
# Convert the request path into a file path, by appending it to the document root from the command line.
# Determine if that file exists. Send an HTTP/1.1 404 response if it does not.
# Open and read the contents of that file, then send the contents back inside an HTTP/1.1 200 OK response.
# Close the connection, as before.
                break
        # this method continues to send data from string until either all data has been sent or an error occurs. \
        # None is returned on success
    conn.close()

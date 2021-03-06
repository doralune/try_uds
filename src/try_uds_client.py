# -*- coding: utf-8 -*-
__author__="Pichai Kankuekul"
__copyright__="Copyright 2017, XCompass Intelligence Ltd."

'''
Try client using Unix Domain Socket (UDS)
'''

import pdb
import argparse
import os
import sys
import socket
from cPickle import dumps, loads
import numpy as np

def init():
    server_address = "./uds/dummy"
    mode = "msg"

    parser = argparse.ArgumentParser()
    parser.add_argument("--server_address",  default=server_address)
    parser.add_argument("--mode", default=mode)
    args = parser.parse_args()

    return args

def do_msg(sock):
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

def do_size_msg(sock):
    message = 'This is full message.'
    size    = '%16d' % len(message)
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(size)
    sock.sendall(message)

def do_list(sock):
    #a_list = [3, 1, 4, 1, 5, 9, 2]
    #a_list = [3, 1, '4', 1, 5, 9, 2]
    a_list = [3, 1, '4', np.array([1, None]), 5, 9, 2]
    message = dumps(a_list)

    num = int(np.ceil(1.0 * len(message) / 16))
    print >>sys.stderr, 'sending "%s" in %s times' % (a_list, num)

    num = '%16d' % num
    sock.sendall(num)
    sock.sendall(message)

def run(args):
    # create a socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    print >>sys.stderr, 'connecting to %s' % args.server_address
    try:
        sock.connect(args.server_address)
    except socket.error, msg:
        print >>sys.stderr, msg
        sys.exit(1)

    try:
        # Send data
        if 'msg' == args.mode:
            do_msg(sock)
        elif 'size_msg' == args.mode:
            do_size_msg(sock)
        elif 'list' == args.mode:
            do_list(sock)
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()

if  __name__ == "__main__":
    args = init()
    #pdb.set_trace()
    run(args)

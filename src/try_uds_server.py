# -*- coding: utf-8 -*-
__author__="Pichai Kankuekul"
__copyright__="Copyright 2017, XCompass Intelligence Ltd."

'''
Try server using Unix Domain Socket (UDS)
'''

import pdb
import argparse
import os
import sys
import socket
from cPickle import dumps, loads

def init():
    server_address = "./uds/dummy"
    mode = "msg"

    parser = argparse.ArgumentParser()
    parser.add_argument("--server_address", default=server_address)
    parser.add_argument("--mode", default=mode)
    args = parser.parse_args()

    return args

def do_msg(connection):
    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(16)
        print >>sys.stderr, 'received "%s"' % data
        if data:
            print >>sys.stderr, 'sending data back to the client'
            connection.sendall(data)
        else:
            print >>sys.stderr, 'no more data'
            break

def do_size_msg(connection):
    data = connection.recv(16)
    print >>sys.stderr, 'received "%s"' % data
    size = int(data)
    print >>sys.stderr, 'receiving next data in size %d' % size

    amount_received = 0
    amount_expected = size

    data = ""
    while amount_received < amount_expected:
        data += connection.recv(16)
        amount_received += len(data)
    print >>sys.stderr, 'received "%s"' % data

def do_list(connection):
    data = connection.recv(16)
    print >>sys.stderr, 'received "%s"' % data
    num = int(data)
    print >>sys.stderr, 'receiving next data in %d times' % num

    data = ""
    for i in range(num):
        data += connection.recv(16)
    a_list = loads(data)
    print >>sys.stderr, 'received "%s"' % a_list

def run(args):
    # create a socket
    try:
        os.unlink(args.server_address)
    except OSError:
        if os.path.exists(args.server_address):
            raise
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print >>sys.stderr, 'starting up on %s' % args.server_address

    # bind the socket to the port
    parent_dir = os.path.dirname(args.server_address)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    sock.bind(args.server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()

        # Correspond the client
        try:
            print >>sys.stderr, 'connection from', client_address
            if 'msg' == args.mode:
                do_msg(connection)
            elif 'size_msg' == args.mode:
                do_size_msg(connection)
            elif 'list' == args.mode:
                do_list(connection)
        finally:
            connection.close()

if  __name__ == "__main__":
    args = init()
    #pdb.set_trace()
    run(args)

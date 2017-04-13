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

    parser = argparse.ArgumentParser()
    parser.add_argument("--server_address",  default=server_address)
    args = parser.parse_args()

    return args


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

    #
    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        try:
            print >>sys.stderr, 'connection from', client_address

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data)
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
        finally:
            connection.close()

if  __name__ == "__main__":
    args = init()
    #pdb.set_trace()
    run(args)

#!/usr/bin/env python

import sys
import base64
from libs.QGASocket import QGASocket

def fileEncode(handle):
    content = handle.readlines()
    return base64.encodestring(''.join(content))

def uploadFile(socketFile, filename, content):
    conn = QGASocket(socketFile)
    query = {'execute' : 'guest-file-open', 'arguments' : {'path': filename, 'mode' : 'w+'}}
    conn.send(query)
    result = conn.recieve()
    if 'return' not in result.keys() or result['return'] < 0:
        return "File: %s can't be opened!" % filename

    fileHandleId = result['return']

    query  = {'execute' : 'guest-file-write', 'arguments' : {'handle': fileHandleId, 'buf-b64' : content}}

    conn.send(query)
    result = conn.recieve()

    query  = {'execute' : 'guest-file-close', 'arguments' : {'handle': fileHandleId}}
    conn.send(query)
    conn.recieve()
    conn.close()

    if 'return' in result.keys() and result['return']['count'] >= 0 :
        return True
    return False


if __name__ =='__main__':
    if len(sys.argv) < 3 or sys.stdin is None:
        exit(1)

    socketFile = sys.argv[1]
    filename  = sys.argv[2]
    handle = sys.stdin
    content = fileEncode(handle)

    if uploadFile(socketFile, filename, content):
        print "Done"
        exit(0)
    print "Fail"
    exit(1)

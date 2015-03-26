#!/usr/bin/env python

import sys
from libs.QGASocket import QGASocket
import base64

def fetchFile(socketFile, filename):
    conn = QGASocket(socketFile)
    query = {'execute' : 'guest-file-open', 'arguments' : {'path': filename, 'mode' : 'r'}}
    conn.send(query)
    result = conn.recieve()
    if 'return' not in result.keys() or result['return'] < 0:
        return "File: %s can't be opened!" % filename

    fileHandleId =  result['return']

    data = ''
    query= {'execute' : 'guest-file-read', 'arguments' : {'handle': fileHandleId, 'count' : 1<<11}}
    while True:
        conn.send(query)
        result = conn.recieve()
        data += result['return']['buf-b64']
        if result['return']['eof'] :
            break

    query  = {'execute' : 'guest-file-close', 'arguments' : {'handle': fileHandleId}}
    conn.send(query)
    conn.recieve()
    conn.close()

    return base64.decodestring(data)

if __name__ == '__main__':
    if len(sys.argv) < 3 :
        exit(1)

    socketFile = sys.argv[1]
    filename  = sys.argv[2]

    sys.stdout.write( fetchFile(socketFile, filename) )


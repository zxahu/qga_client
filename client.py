#!/usr/bin/env python

import sys
from libs.QGASocket import QGASocket
from libs.Commands import *

if len(sys.argv) < 2 : exit(1)

socketFile = sys.argv[1]

conn = QGASocket(socketFile)
CommandLine = Entry(conn)
CommandLine.do()

conn.close()

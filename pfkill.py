"""
how to it use:
$ python pfkill <port number>

what doing:
1. read <port number>.pid file
2. send signal to running app
3. delete <port number>.rule
4. delete <port number>.pid
"""

import os
import sys
import signal
# import logging

port = sys.argv[1]

# read <port>.pid
pid = int(open("%s.pid" % port, 'r').read().split('\n')[0])

# print pid

# kill app by pid
# signal.SIGQUIT or signal.SIGKILL
try:
    os.kill(pid, signal.SIGQUIT)
except OSError, e:
    print e
    # logging.INFO("ee")

# delete <port>.rule
os.unlink("%s.rule" % port)

# delete <port>.pid
os.unlink("%s.pid" % port)

# todo: exit

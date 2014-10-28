import socket
import sys
import os
import thread
import time
import commands


def main(setup, error):
    # open file for error messages
    sys.stderr = file(error, 'a')
    # read settings for port forwarding
    for forwards in parse(setup):
        print forwards

        # todo: write pid - <port>.pid
        pidwrite("%s.pid" % forwards[0])

        thread.start_new_thread(server, forwards)
    # wait for <ctrl-c>
    while True:
       time.sleep(60)
 

def parse(setup):
    forwards = list()
    for line in file(setup):
        parts = line.split()
        forwards.append((int(parts[0]), parts[1], int(parts[2])))
    return forwards
 

def server(*forwards):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind((interface2ip(), forwards[0]))
        dock_socket.listen(5)
        while True:
            client_socket = dock_socket.accept()[0]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((forwards[1], forwards[2]))
            thread.start_new_thread(forward, (client_socket, server_socket))
            thread.start_new_thread(forward, (server_socket, client_socket))
    finally:
        thread.start_new_thread(server, forwards)
 

def interface2ip():
    intf = open("interface.conf", 'r').read().split('\n')[0]
    intf_ip = commands.getoutput("ip address show dev " + intf).split()
    intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
    return intf_ip


def forward(source, destination):
    string = ' '
    while string:
        string = source.recv(1024)
        if string:
            destination.sendall(string)
        else:
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)


# todo: rename
def pidwrite(pidfile):
    pfile = open(pidfile, "w+")

    pfile.write("%s" % str(os.getpid()))
    pfile.close()


if __name__ == '__main__':
    # todo: make
    conf = "%s.rule" % sys.argv[1]
    log  = "%s.log" % sys.argv[1]
    main(conf, log)

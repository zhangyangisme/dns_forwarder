#!/usr/bin/env python

import socket
import struct
import threading
import Queue
import sqlite3

class Consumer(threading.Thread):
    def __init__(self,arg):
        super(Consumer,self).__init__()
        self.queue = arg
    def run(self):
        while True:
            sock,request_data,address = self.queue.get()
            print "get request:",address
            response = send_request(request_data)
            sock.sendto(response,address)



def send_request(request):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    sock.connect(("114.114.114.114",53))
    request_length = len(request)
    print request_length
    length = struct.pack("!H",request_length)
    sock.send(length)
    sock.send(request)
    response_length = sock.recv(2)
    response = sock.recv(1024)
    sock.close()
    return response

def forward_udp_dns(udp_sock):
    queues = []
    for i in range(3):
        queue = Queue.Queue()
        t = Consumer(queue)
        queues.append(queue)
        t.setDaemon(False)
        t.start()
    while True:
        i = 0
        try:
            request_data,address = udp_sock.recvfrom(1024)
            print address
            queues[i].put((udp_sock,request_data,address))
            i = i + 1
            if(i == 3):
                i = 0
        except Exception,e:
            print "socket error",Exception,":",e


def local_server():
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("127.0.0.1",53))
    udp_sock.setblocking(1)
    forward_udp_dns(udp_sock)

def main():
    local_server()

if __name__ == "__main__":
    main()

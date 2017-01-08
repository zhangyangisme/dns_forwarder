#!/usr/bin/env python

import socket
import struct
import threading
import Queue
import logging
import sqlite3

class Consumer(threading.Thread):
    def __init__(self,arg):
        super(Consumer,self).__init__()
        self.queue = arg
        self.count = 0
    def run(self):
        while True:
            sock,request_data,address = self.queue.get()
            logging.info("get_request:%s"%str(address))
            try:
                response = send_request(request_data)
                sock.sendto(response,address)
                self.count = self.count + 1
                if(self.count %50 == 0):
                    logging.info("thread %s forward request %d"%(self.getName(),self.count))
            except Exception,e:
                logging.exception("thread %s"%self.getName())

def send_request(request):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    sock.connect(("114.114.114.114",53))
    request_length = len(request)
    length = struct.pack("!H",request_length)
    sock.send(length)
    sock.send(request)
    response_length = sock.recv(2)
    response = sock.recv(1024)
    sock.close()
    return response

def forward_udp_dns(udp_sock):
    queues = []
    for i in range(4):
        queue = Queue.Queue()
        t = Consumer(queue)
        queues.append(queue)
        t.setDaemon(False)
        t.setName(str(i))
        t.start()
    while True:
        if i == 4:
            i = 0
        try:
            request_data,address = udp_sock.recvfrom(1024)
        except Exception,e:
            logging.exception("loged")
        else:
            queues[i].put((udp_sock,request_data,address))
            i = i + 1

def local_server():
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("127.0.0.1",53))
    udp_sock.setblocking(1)
    forward_udp_dns(udp_sock)

def main():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%y-%m-%d %H:%M:%S',
                filename='dns_forwarder.log',
                filemode='a+')
    local_server()

if __name__ == "__main__":
    main()

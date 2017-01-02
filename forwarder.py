#!/usr/bin/env python

import socket
import struct


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

def forward_udp_dns(sock):
    while True:
        request_data,address = sock.recvfrom(1024)
        print address
        response = send_request(request_data)
        sock.sendto(response,address)


def local_server():
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    udp_sock.bind(("127.0.0.1",53))
    forward_udp_dns(udp_sock)

def main():
    local_server()

if __name__ == "__main__":
    main()

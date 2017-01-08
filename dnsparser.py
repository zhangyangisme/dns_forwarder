#!/usr/bin/env python

import struct


'''dns header struct
struct dns_header{
    unsigned char qr:1;
    unsigned char opcode:4;
    unsigned char aa:1;
    unsigned char rd:1;

    unsigned char ra:1;
    unsigned char z:1;
    unsigned char ad:1;
    unsigned char cd:1;
    unsigned char rcode:4;
};

'''

DNS_HEADER_LENGTH = 12


class Dns_Request(object):
    def __init__(self):
        self.domain = None
        self.qry_type = None
        self.qry_class = None
        return
    

def dns_request_parser(dns_request):
    request_header = dns_request[:12]
    body = dns_request[12:]
    body_lenght = len(body)
    domain = ""
    cur = 0
    while cur < body_lenght:
        field_len = int(body[cur])
        cur  = cur + 1
        domain = domain + str(body[cur:field_len])
        cur = cur + field_len
        if field_len == 0:
            break
    qry_type = struct.unpack("!H",body[cur:cur+2])
    cur = cur + 2
    qry_class = struct.unpack("!L",body[cur:])
    
    dns_request = Dns_Request()
    dns_request.domain = domain
    dns_request.qry_type = qry_type
    dns_request.qry_class = qry_class


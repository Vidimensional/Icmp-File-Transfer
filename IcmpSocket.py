#-*- coding: utf-8 -*-

from socket import *
from IcmpPacket import IcmpPacket

class IcmpSocket (object):
    
    def __init__ (self):
        self.socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

    def recv (self):
        return IcmpPacket(raw_p=self.socket.recv(1024)[20:])

    def sendto (self, packet, dst_addr):
        self.socket.sendto(packet.packet, (dst_addr,1))
        



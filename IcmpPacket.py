#-*- coding: utf-8 -*-


#    IcmpPacket: Little library to manage icmp protocol
#    Copyright (C) 2012 Daniel Vidal de la Rubia
#    
#    Based on ping.py package by George Notaras 
#    http://www.g-loaded.eu/2009/10/30/python-ping/

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import struct
import socket

ECHO_REPLY = 0
# (...)
ECHO_REQUEST= 8
# (...)

ICMP_PACKET_SIZE = 64
ICMP_PAYLOAD_SIZE = ICMP_PACKET_SIZE - 8

class IcmpPacket (object):

    def __init__ (self, type_packet=0, code=0, seq_n=0, payload=0, raw_p=None):
        if raw_p :
            p = struct.unpack('bbHHh56s', raw_p)
            self.type_packet = p[0]
            self.code = p[1] 
            self.checksum = p[2]
            self.identifier = p[3]
            self.seq_n = p[4]
            self.payload = p[5]
        else:
            self.type_packet = type_packet
            self.code = code
            self.checksum = 0
            self.identifier = os.getpid() & 0xFFFF
            self.seq_n = seq_n
            self.payload = payload
            
            self.packet = None

            header_fmt = 'bbHHh'
            payload_fmt = '%ds' % (ICMP_PAYLOAD_SIZE)
            packet_fmt = '!' + header_fmt + payload_fmt

            self.packet = struct.pack(packet_fmt, self.type_packet, self.code, 
                                      self.checksum, self.identifier, 
                                      self.seq_n, str(self.payload))
            self.calcule_checksum()
            self.packet = struct.pack(packet_fmt, self.type_packet, self.code, 
                                      self.checksum, self.identifier, 
                                      self.seq_n, str(self.payload))
                                      

    def __repr__ (self):
        if self.type_packet is ECHO_REPLY:
            type_packet = 'ECHO_REPLY'
        elif self.type_packet is ECHO_REQUEST:
            type_packet = 'ECHO_REQUEST'
        else:
            print "TODO: añadir moar tipos: %d" % (self.type_packet)
            type_packet = 'NOT_DEFINED_BY_IcmpPacket'

        return "ICMP "+ type_packet +" seq:" + str(self.seq_n) +" payload:" +\
               self.payload
    

    def calcule_checksum (self):
        """
        I'm not too confident that this is right but testing seems
        to suggest that it gives the same answers as in_cksum in ping.c
        """
        sum = 0
        countTo = (len(self.packet)/2)*2
        count = 0
        while count<countTo:
            thisVal = ord(self.packet[count + 1])*256 + \
                      ord(self.packet[count])
            sum = sum + thisVal
            sum = sum & 0xffffffff # Necessary?
            count = count + 2
     
        if countTo<len(self.packet):
            sum = sum + ord(self.packet[len(self.packet) - 1])
            sum = sum & 0xffffffff # Necessary?
     
        sum = (sum >> 16)  +  (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
     
        # Swap bytes. Bugger me if I know why.
        answer = answer >> 8 | (answer << 8 & 0xff00)
     
        self.checksum = answer


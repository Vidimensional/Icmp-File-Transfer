#!/usr/bin/env python
#-*- coding: utf-8 -*-


#    Copyright (C) 2012 Daniel Vidal de la Rubia
#
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

import socket
import sys
 

from IcmpPacket import *

action = sys.argv[1]
filename = sys.argv[2]
if action == 'send':
    dst_addr = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

def send_icmp (s, packet):
    s.sendto(packet.packet, (dst_addr,1))

def recv_icmp (s):
    packet = IcmpPacket(raw_p=s.recv(1024)[20:])
    return packet

if action == 'send': 
    mode = 'r'
    f = open(filename, mode)

    seq_n = 0
    while True: 
        data = f.read(56)
        if not data:
            packet = IcmpPacket(ECHO_REQUEST, seq_n=seq_n, payload=data, 
                                code=2)
            send_icmp(s, packet)
            break
        packet = IcmpPacket(ECHO_REQUEST, seq_n=seq_n, payload=data)
        send_icmp(s, packet)
        seq_n += 1

elif action == 'recv': 
    mode = 'w'
    f = open(filename, mode)
    buff = []
    while True:
        icmp = recv_icmp(s)
        if icmp.code is 2: break
        buff.append((icmp.seq_n, icmp.payload))
    buff.sort()
    str_buff = ''
    for elem in buff:
        str_buff += buff
    print str_buff
        

    





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

#import socket
import sys
 

from IcmpPacket import *
from IcmpSocket import *

action = sys.argv[1]
filename = sys.argv[2]
if action == 'send':
    dst_addr = sys.argv[3]

#s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
icmp_socket = IcmpSocket()

if action == 'send': 
    mode = 'r'
    f = open(filename, mode)

    seq_n = 0
    while True: 
        data = f.read(56)
        if not data:
            packet = IcmpPacket(ECHO_REQUEST, seq_n=seq_n, payload=data, 
                                code=2)
            icmp_socket.sendto(packet, dst_addr)
            break
        packet = IcmpPacket(ECHO_REQUEST, seq_n=seq_n, payload=data)
        icmp_socket.sendto(packet, dst_addr)
        seq_n += 1

elif action == 'recv': 
    mode = 'w'
    f = open(filename, mode)
    buff = []
    while True:
        icmp = icmp_socket.recv()
        if icmp.code is 2: break
        buff.append((icmp.seq_n, icmp.payload))
    buff.sort()
    str_buff = ''
    for elem in buff:
        str_buff += elem[1]
    f.write(str_buff) 

    





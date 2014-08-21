#-*- coding: utf-8 -*-

#    Copyright (C) 2012-2014 Daniel Vidal de la Rubia
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>

from socket import *
from IcmpPacket import IcmpPacket

class IcmpSocket (object):
    
    def __init__ (self):
        self.socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

    def recv (self):
        return IcmpPacket(raw_p=self.socket.recv(1024)[20:])

    def sendto (self, packet, dst_addr):
        self.socket.sendto(packet.packet, (dst_addr,1))
        



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

from IcmpSocket import *
from IcmpPacket import *


class IcmpApp (object):
    def __init__ (self):
        self.socket = IcmpSocket()
        self.file = None

    def __enter__ (self):
        return self

    def __exit__ (self, type, value, traceback):
        if self._file is not None and not self._file.closed:
            self._file.closed


class IcmpSender (IcmpApp):

    def __init__ (self, file_to_send):
        super(IcmpSender, self).__init__()
        self._file = open(file_to_send, 'r')

    def send (self, dst_addr):
        seq_n = 0
        while True: 
            data = self._file.read(56)
            if not data:
                packet = IcmpPacket(ECHO_REQUEST, seq_n=seq_n, payload=data, 
                                    code=2)
                self.socket.sendto(packet, dst_addr)
                break
            packet = IcmpPacket(ECHO_REQUEST, seq_n=seq_n, payload=data)
            self.socket.sendto(packet, dst_addr)
            seq_n += 1
        


class IcmpReceiver (IcmpApp):
    
    def __init__ (self, file_to_receive):
        super(IcmpReceiver, self).__init__()
        self._file = open(file_to_receive, 'w')

    def receive (self):
        buff = []
        while True:
            icmp = self.socket.recv()
            if icmp.code is 2: break
            buff.append((icmp.seq_n, icmp.payload))
        buff.sort()
        str_buff = ''
        for elem in buff:
            str_buff += elem[1]
        self._file.write(str_buff) 



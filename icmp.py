#!/usr/bin/env python
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys

#from IcmpPacket import *
#from IcmpSocket import *
from IcmpApp import IcmpSender, IcmpReceiver

action = sys.argv[1]
filename = sys.argv[2]
if action == 'send':
    dst_addr = sys.argv[3]

#icmp_socket = IcmpSocket()

if action == 'send': 
    with IcmpSender(filename) as sender:
        sender.send(dst_addr)
elif action == 'recv': 
    with IcmpReceiver(filename) as receiver:
        receiver.receive()
    




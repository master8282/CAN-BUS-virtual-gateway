#!/usr/bin/env python3
# Virtual CAN GW connects CAN0 CAN1, the GW is based on
# raspberry Pi3b and two MCP2525 boards.
# The gw plugs in between two can devices.
# The goal is marking incoming traffic, to see
# diffrence what comes and what leaves from device.
# For marking I used "ERR" bit, many devices don't pay
# attention for "ERR", but wireshark identifies it
# and you are able to see incoming and outgoing packets.
# I used it for reverce engineering for tracking my car stereo
# packets. It helped me much, hope it would help you too.

from threading import Thread
import can
import sys

bus0 = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=83333)
bus1 = can.interface.Bus(bustype='socketcan', channel='can1', bitrate=83333)

def send_oneside():

    while True:
        msg1recv = bus1.recv(1)

        if msg1recv and msg1recv.is_error_frame == False:

            msg0send = can.Message(arbitration_id = msg1recv.arbitration_id,
                                   extended_id = False, data = msg1recv.data, is_error_frame = True)

            try:
                bus0.send(msg0send)
            except can.CanError:
                print("Message in bus0 NOT sent")

def send_second():

    while True:
        msg0recv = bus0.recv(1)

        if msg0recv and msg0recv.is_error_frame == False:

            msg1send = can.Message(arbitration_id = msg0recv.arbitration_id,
                                   extended_id = False, data = msg0recv.data, is_error_frame = True)

            try:
                bus1.send(msg1send)
            except can.CanError:
                print("Message in bus1 NOT sent")



def app_start():

    can0to1 = Thread(target=send_oneside)
    can1to0 = Thread(target=send_second)

    can0to1.start()
    can1to0.start()

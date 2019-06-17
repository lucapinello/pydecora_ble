#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# Copyright (c) 2019 Luca Pinello
# MIT license
#This code was inspired by https://github.com/mjg59/python-decora (this doesn't work with the latest firmware)

__version__ = "0.1.0"
import time
class BLE_Device(object):

    def __init__(self,mac,backend='bluepy'):

        self.connected=False
        self.backend=None
        self.device=None
        self.adapter=None
        self.mac=mac

        if backend=='pygatt':
            from pygatt import GATTToolBackend
            self.backend_class=GATTToolBackend

        elif backend=='bluepy':
            from bluepy import btle
            self.backend_class=btle

        self.backend=backend

    def connect(self):

        if self.backend=='pygatt':
            self.adapter = self.backend_class('hci0')
            self.adapter.reset()
            self.adapter.start(False)
            self.device=self.adapter.connect(self.mac)

        elif self.backend=='bluepy':
            self.device=self.backend_class.Peripheral(self.mac, addrType=self.backend_class.ADDR_TYPE_PUBLIC)

    def write_handle(self,handle,packet,wait=True):
        if self.backend=='pygatt':
            self.device.char_write_handle(handle,packet,wait_for_response=wait)

        elif self.backend=='bluepy':
            self.device.writeCharacteristic(handle, packet, withResponse=wait)

    def read_handle(self,handle):
        if self.backend=='pygatt':
            return self.device.char_read_handle(handle)

        elif self.backend=='bluepy':
            return self.device.readCharacteristic(handle)

    def list_chars(self):

        if self.backend=='pygatt':
            return self.device.discover_characteristics().values()
        elif self.backend=='bluepy':
            return self.device.getCharacteristics()

    def disconnect(self):

        if self.device:

            if self.backend=='pygatt':

                self.device.disconnect()
                self.adapter.stop()

            elif self.backend=='bluepy':
                self.device.disconnect()


def get_decora_ble_key(mac,backend='bluepy'):
    if backend=='bluepy':
        device=BLE_Device(mac,'bluepy')
        time.sleep(1)
        device.connect()
        device.write_handle(0x37, bytearray([0x22, 83, 0x00, 0x00, 0x00, 0x00]))
        rawkey=device.read_handle(0x37)
        if rawkey=='"SLEVI':
            print("Switch is not in pairing mode - hold down until green light flashes and execute this function again\n")
        else:
            rawkey=str(bytearray('0x11')+bytearray(rawkey)[1:])
            print('The key for your device is:'+repr(rawkey))
        device.disconnect()
    else:
        print('This function is not supported with the pygatt backend')



class Decora_BLE(object):

    def __init__(self,mac,key,backend='bluepy'):


        self.device=BLE_Device(mac,backend=backend)
        self.backend=backend

        if isinstance(key, str):
            self.key = bytearray(key)
        else:
            raise Exception('expected a string like this:'+r'\x11S\x8dVW\xc2')

        self.power=0
        self.level=0

    def connect(self):
            self.device.connect()
            self.device.write_handle(0x37,self.key)

            self.device.write_handle(0x26,bytearray([0x01,0x00]))
            self.device.write_handle(0x3d,bytearray([0xe3,0x07,0x06,0x0f]))
            self.device.write_handle(0x3a,bytearray([0x15,0x15,0x19]))

            if self.backend=='bluepy':
                self.power,self.level=bytearray(self.device.read_handle(0x25))

    def get_state(self):
        self.power,self.level=bytearray(self.device.read_handle(0x25))
        return self.power, self.level

    def on(self,force_update=False):
        if force_update and self.backend=='bluepy':
            self.get_state()
        else:
            self.power=1
            self.device.write_handle(0x25, bytearray([self.power,self.level]))

    def off(self,force_update=False):

        if force_update and self.backend=='bluepy':
            self.get_state()
        else:
            self.power=0
            self.device.write_handle(0x25, bytearray([self.power,self.level]))

    def set_level(self,level,force_update=False):
        if force_update and self.backend=='bluepy':
            self.get_state()
        else:
            self.level=level
            self.device.write_handle(0x25, bytearray([self.power,self.level]))

    def disconnect(self):
        if self.device:
            self.device.disconnect()

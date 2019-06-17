#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# Copyright (c) 2019 Luca Pinello
# MIT license
#This code was inspired by https://github.com/mjg59/python-decora (this doesn't work with the latest firmware)

import os
from setuptools import setup
from setuptools import find_packages

import re

version = re.search(
    	'^__version__\s*=\s*"(.*)"',
    	open('decora_ble/__init__.py').read(),
    	re.M
    	).group(1)

setup(
    name='decora_ble',
    version=0.1,
    description='A Python module to interact with the Leviton Decora Dimmer via Bluetooth (BLE)',
    url='https://github.com/lucapinello/pydecora_ble',
    author='Luca Pinello',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'bluepy', #pygatt is also supported
    ]
)

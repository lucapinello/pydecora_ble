# pydecora_ble

Python module to interact with Leviton dimmers (for example this one:https://www.leviton.com/en/products/ddl06-blz) via Bluetooth (BLE).

This code was inspired by https://github.com/mjg59/python-decora (unfortunately this doesn't work anymore with the latest firmware).

## 0. Requirements
Linux, Python (>=2.7 or >=3.5) and  bluepy (https://github.com/Chaffelson/blupy)
(pypygatt >=4.0.3 is also partially supported https://github.com/peplin/pygatt)

This package as been tested on a RasperryPI ZeroW with Raspbian GNU/Linux 9 (stretch)

## 1. Install with:

`pip install pydecora_ble`

## 2. Short example

First it is necessary to get the key from the device (this is necessary only one time).

Press and hold the down button for 3 seconds and then execute this function.

`get_decora_ble_key("F0:C7:7F:09:15:41")`

Here "F0:C7:7F:09:15:41" is the physical address of your device.

This will return a message with the key:

`The key for your device is:'0x11S\x8dVW\xc2'`

Then you can create the object with:

`d=Decora_BLE(mac="F0:C7:7F:09:15:41",key='\x11S\x8dVW\xc2')`

Then connect with:

`d.connect()`

To turn it on and off use:

` d.on()`

or

`d.off()`

To change the level use (any number between 0-100).

`d.set_level(54)`

You can read the current state with:

`power,level=d.get_state()`

Here power is 1 for on and 0 for off.

To disconnect:

`d.disconnect()`



# main game
# pong game that supports single and 2 player
# 2 player mode requres 2 arduino devices connected to the computer via BLE

import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient

import game

# discover devices
async def discover(mode):
    # search for devices
    devices = await BleakScanner.discover()
    print("Devices detected: ")
    i = 1
    for d in devices:
        print("|", i, "|", d)
        i += 1
    
    # select device to connect to
    num1 = input("Select player 1: ")
    if mode == 2:
        num2 = input("Select player 2: ")
    else:
        num2 = 1
    return devices[int(num1)-1], devices[int(num2)-1]


async def main():
    # get game modes and devices
    mode = input("Single player (1) / 2 player (2):")
    mode = int(mode)
    try:
        device1, device2 = await discover(mode)
    except e:
        print("ERROR: invalid input")


    # connect to device(s)
    if mode == 1: # single player mode
        # set up gui
        gui = game.Game(True)
        await asyncio.gather(connect(1, gui, device1))
    else: # 2 player mode
        # set up gui
        gui = game.Game(False)
        await asyncio.gather(connect(1, gui, device1), connect(2, gui, device2))


async def connect(id, gui, device):
    print("starting", device, "loop")
    async with BleakClient(device) as client:
        print("connect to", device)
        # Assumes the bluetooth device sends all IMU data in a a 24-byte array
        for service in client.services:
            for char in service.characteristics:
                if "read" in char.properties:
                    # Assumes there's only one readable characteristic
                    try:
                        while(not gui.exit):
                            # Read value and update bar position
                            value = bytes(await client.read_gatt_char(char.uuid))
                            IMU = byteToFloat(value)
                            gui.update_bar_offset(id, IMU[1])
                            gui.update_frame()
                            # for debugging
                            #print(device)
                            #printIMU(IMU)

                            await asyncio.sleep(0)
                    except Exception as e:
                        print(e)
                    finally:
                        await client.disconnect()

    print("disconnect from", device)

# convert byte array to float array
def byteToFloat(arr):
    floats = []
    for i in range(6):
        floats.append(struct.unpack('f', arr[4*i:(4*i)+4])[0])
    return floats

# print IMU values (for debugging)
def printIMU(arr):
    types = ["ax", "ay", "az", "gx", "gy", "gz"]
    for i in range(6):
        print(types[i], ":", arr[i], end="\t")
    print()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = main()
    loop.run_until_complete(task)

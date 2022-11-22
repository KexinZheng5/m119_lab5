# IMU visualization (part of the pong game)
# uses the acceleration for x to control the position of a bar

import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient

import game

uuid = "00002a57-0000-1000-8000-00805f9b34fb"
   
# discover devices
async def discover():
    # search for devices
    devices = await BleakScanner.discover()
    print("Devices detected: ")
    i = 1
    for d in devices:
        print("|", i, "|", d)
        i += 1
    
    # select device to connect to
    num = input("Connect to device: ")
    return devices[int(num)-1]

# connect to device
async def connect(device, gamemode):
    # connect to selected device
    async with BleakClient(device) as client:
        print(f"Connected to: {device.name}")

        # initializes the game gui
        gui = game.Game()
        gui.initialize(gamemode)
        
        # Assumes the bluetooth device sends all IMU data in a a 24-byte array
        for service in client.services:
            for char in service.characteristics:
                if "read" in char.properties:
                    # Assumes there's only one readable characteristic
                    try:
                        while(gui.exit == False):
                            # Read value and update bar position
                            value = bytes(await client.read_gatt_char(char.uuid))
                            IMU = byteToFloat(value)
                            gui.update_frame(IMU[0]) # bar is controlled by ax
                        
                    except Exception as e:
                        print("ERROR:", e)
                    finally:
                        await client.disconnect()

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

# main program
async def main():
    try:
        device = await discover()
    except e:
        print("ERROR: invalid input")

    await connect(device, True)

if __name__ == "__main__":
    asyncio.run(main())
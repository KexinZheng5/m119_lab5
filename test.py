import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient

import game

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
    num1 = input("Select player 1: ")
    num2 = input("Select player 2: ")
    return devices[int(num1)-1], devices[int(num2)-1]


async def main():
    try:
        device1, device2 = await discover()
    except e:
        print("ERROR: invalid input")

    gui = game.Game(False)
    #devices = [device1, device2]
    await asyncio.gather(connect(1, device1), connect(2, device2))
    #await asyncio.gather(*(connect(device) for device in devices))


async def connect(id, device):
    print("starting", device, "loop")
    async with BleakClient(device) as client:
        print("connect to", device)
        # Assumes the bluetooth device sends all IMU data in a a 24-byte array
        for service in client.services:
            for char in service.characteristics:
                if "read" in char.properties:
                    # Assumes there's only one readable characteristic
                    try:
                        while(True):
                            # Read value and update bar position
                            value = bytes(await client.read_gatt_char(char.uuid))
                            IMU = byteToFloat(value)
                            print(device)
                            printIMU(IMU)
                            # 
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
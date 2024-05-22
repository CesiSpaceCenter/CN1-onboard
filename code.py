import time

import board
import busio
import digitalio

from acc import Accelerometer
from baro import Barometer
import storage

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

hc12 = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=9600)
acc = Accelerometer()
baro = Barometer()


storage.remount("/", readonly=False)

led.value = True
acc.calibrate()
baro.calibrate()
led.value = False

filename = 'data.txt'

buffer = b''
n_packets = 0

while True:
    led.value = True
    data = []
    acc.get()
    data.append(time.monotonic())
    data.extend(acc.acceleration)
    data.extend(acc.orientation)
    baro.get()
    data.append(baro.pressure)
    data.append(baro.altitude)
    data.append(baro.temperature)
    packet = (",".join([str(val) for val in data])).encode() + b'\n' # join every data item with a comma
    hc12.write(packet)
    buffer += packet
    if n_packets == 10: # if 10 packets have been captured
        n_packets = 0
        # save to a file
        with open(filename, 'ab') as file:
            file.write(buffer)
            buffer = b''
    n_packets += 1
    led.value = False
    time.sleep(0.1)

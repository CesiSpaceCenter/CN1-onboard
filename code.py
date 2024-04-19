import board
import busio
import digitalio
import time
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

buffer = b''
i_buf = 0
_i = 0

while True:
    led.value = True
    data = []
    acc.get()
    data.extend(acc.acceleration)
    data.extend(acc.orientation)
    baro.get()
    data.append(baro.pressure)
    data.append(baro.altitude)
    data.append(baro.temperature)
    data_enc = (",".join([str(val) for val in data])).encode() + b'\n'  + str(_i).encode()+ b'\n'
    hc12.write(data_enc)
    buffer += data_enc
    if i_buf == 10:
        i_buf = 0
        with open('data.txt', 'wb') as file:
            file.write(buffer)
    i_buf += 1
    _i += 1
    led.value = False
    time.sleep(0.1)
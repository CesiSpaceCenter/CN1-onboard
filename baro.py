import time
import board
import adafruit_bmp280
import busio

class Barometer:
    def __init__(self):
        self.i2c = busio.I2C(scl=board.GP11, sda=board.GP10)   # uses board.SCL and board.SDA
        self.bmp = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c)
        
    def calibrate(self):
        cal_avg = []
        n_cal = 100
        for i in range(n_cal):
            cal_avg.append(self.bmp.pressure)
            time.sleep(0.03)
        
        self.bmp.sea_level_pressure = sum(cal_avg)/n_cal
        print('BMP Calibration value:', self.bmp.sea_level_pressure)
        return self.bmp.sea_level_pressure
        
    pressure = 0
    altitude = 0
    temperature = 0
    def get(self):
        self.pressure = self.bmp.pressure
        self.altitude = self.bmp.altitude
        self.temperature = self.bmp.temperature
import time
import board
import busio
import adafruit_bmp280
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33

class Accelerometer:
    def __init__(self):
        self.i2c = busio.I2C(board.GP17, board.GP16)
        self.lsm = LSM6DS33(self.i2c, 0x6b)

    def calibrate(self):
        cal_avg_acc = ([], [], [])
        cal_avg_gyro = ([], [], [])
        n_cal = 100
        for i in range(n_cal):
            gyro_x, gyro_y, gyro_z = self.lsm.gyro
            cal_avg_gyro[0].append(gyro_x)
            cal_avg_gyro[1].append(gyro_y)
            cal_avg_gyro[2].append(gyro_z)
            
            accel_x, accel_y, accel_z = self.lsm.acceleration
            cal_avg_acc[0].append(accel_x)
            cal_avg_acc[1].append(accel_y)
            cal_avg_acc[2].append(accel_z)
            time.sleep(0.03)

        self.cal_gyro = (
            sum(cal_avg_gyro[0])/n_cal,
            sum(cal_avg_gyro[1])/n_cal,
            sum(cal_avg_gyro[2])/n_cal
        )
        self.cal_acc = (
            sum(cal_avg_acc[0])/n_cal,
            sum(cal_avg_acc[1])/n_cal,
            sum(cal_avg_acc[2])/n_cal
        )
        
        print('LSM Calibration value:', self.cal_gyro, self.cal_acc)
        return self.cal_gyro, self.cal_acc

    orientation = [0, 0, 0]
    acceleration = [0, 0, 0]
    last_measurement = time.monotonic()
    def get(self):
        dt = time.monotonic() - self.last_measurement
        accel_x, accel_y, accel_z = self.lsm.acceleration
        gyro_x, gyro_y, gyro_z = self.lsm.gyro
        
        accel_x -= self.cal_acc[0]
        accel_y -= self.cal_acc[1]
        accel_z -= self.cal_acc[2]
        
        gyro_x -= self.cal_gyro[0]
        gyro_y -= self.cal_gyro[1]
        gyro_z -= self.cal_gyro[2]
        
        self.acceleration[0] += accel_x * dt
        self.acceleration[1] += accel_y * dt
        self.acceleration[2] += accel_z * dt
        
        self.orientation[0] += gyro_x * dt  # Roulis
        self.orientation[1] += gyro_y * dt  # Tangage
        self.orientation[2] += gyro_z * dt  # Lacet
        
        self.last_measurement = time.monotonic()
import time
import board
import busio
import adafruit_adxl34x

# 初始化I2C和加速度計
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# 初始化變數
velocity = [0, 0, 0]
displacement = [0, 0, 0]
last_time = time.time()

while True:
    # 獲取當前時間和時間間隔
    current_time = time.time()
    dt = current_time - last_time

    # 獲取加速度數據
    acceleration = accelerometer.acceleration

    # 計算速度和位移
    for i in range(3):
        velocity[i] += acceleration[i] * dt
        displacement[i] += velocity[i] * dt

    # 更新時間
    last_time = current_time

    # 輸出加速度、速度和位移
    print("Acceleration: %f %f %f" % acceleration)
    print("Velocity: %f %f %f" % tuple(velocity))
    print("Displacement: %f %f %f" % tuple(displacement))

    time.sleep(0.1)

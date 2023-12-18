import time
import json
import board
import busio
import adafruit_adxl34x

# 初始化I2C和加速度計
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# 初始化變數
velocity = [0, 0, 0]
displacement = [0, 0, 0]

# 添加一個小的延遲，讓第一個記錄的時間是從 0 點多開始
time.sleep(0.1)

start_time = time.time()  # 儲存開始的時間
last_time = start_time  # 初始化 last_time

data = []  # 儲存所有的數據

while True:
    # 獲取當前時間和時間間隔
    current_time = time.time()
    elapsed_time = current_time - start_time  # 計算經過的時間
    dt = current_time - last_time

    # 獲取加速度數據
    acceleration = accelerometer.acceleration

    # 計算速度和位移
    for i in range(3):
        velocity[i] += acceleration[i] * dt
        displacement[i] += velocity[i] * dt

    # 更新時間
    last_time = current_time

    # 將數據添加到列表中
    data.append({
        'time': elapsed_time,  # 使用經過的時間
        'acceleration': acceleration,
        'velocity': velocity,
        'displacement': displacement
    })

    # 輸出加速度、速度和位移
    print(data[-1])

    time.sleep(0.1)

    # 每5秒保存一次數據
    if int(current_time) % 5 == 0:
        with open('data.json', 'w') as f:
            json.dump(data, f)

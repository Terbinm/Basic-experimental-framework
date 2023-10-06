#讀取config
from function.ConfigLoader import ConfigLoader
from datetime import datetime




#開始錄音
from function.PMBRecording import UartGetTLVdata
import serial

if __name__ == "__main__":
    config_data = ConfigLoader('config').config_dict

    now = datetime.now()
    timestamp = str(now.strftime("%Y-%m-%d %H-%M-%S"))

    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
    uartGetTLVdataObj = UartGetTLVdata(timestamp, port, 50)  # 在這裡設定自定義暫停點
    uartGetTLVdataObj.run()

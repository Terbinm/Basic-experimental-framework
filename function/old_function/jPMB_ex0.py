import serial
import struct
import datetime
import json
import time
from mmWave import peopleMB

class globalV:
    count = 0
    def __init__(self, count):
        self.count = count

port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

gv = globalV(0)
pm = peopleMB.PeopleMB(port)

def v6Unpack(v6Data):
    print("---v6解包---")

def v7UnpackXY(v7Data):
    print("---v7解包---")
    v7xy = []
    for k in v7Data:
        v7xy.append({"位置X": k[1], "位置Y": k[2]})   
    return v7xy
    
def v7UnpackVelocityXY(v7Data): # 速度 X, Y
    velxy = []
    for k in v7Data:
        velxy.append({"速度X": k[3], "速度Y": k[4]})
    return velxy

def uartGetTLVdata(name):
    data = {
        "数据": [],
        "TLV数量": {
            "v6": 0,
            "v7": 0,
            "v8": 0
        }
    }
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    print("mmWave:人员移动行为 {:} 示例:".format(name))
    pt = datetime.datetime.now()
    ct = datetime.datetime.now()
    port.flushInput()
    pm.useDebug(True)
    
    collecting_data = True  # 添加一个标志变量来控制数据采集

    try:
        while collecting_data:
            ct = datetime.datetime.now()
            (dck, v6, v7, v8) = pm.tlvRead(False)
            hdr = pm.getHeader()
            if dck:
                print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})] {}\n".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8),ct-pt))
                pt = ct
                xy = v7UnpackXY(v7)
                print("位置[X,Y]:",xy)
                vxy = v7UnpackVelocityXY(v7)
                print("速度[X,Y]:",vxy)
                # 更新TLV数量
                data["TLV数量"]["v6"] = len(v6)
                data["TLV数量"]["v7"] = len(v7)
                data["TLV数量"]["v8"] = len(v8)
                #print(f"v6 length: {len(v6)}, v7 length: {len(v7)}, v8 length: {len(v8)}")
                with open('data.json', 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    timestamp = ct.strftime("%Y-%m-%d %H:%M:%S.%f")
                    data["数据"].append({"检测数": hdr.frameNumber, "时间戳": timestamp, "位置": xy, "速度": vxy,"v6數量": len(v6),  # 修正這裡
                    "v7數量": len(v7),  # 修正這裡
                    "v8數量": len(v8)   # 修正這裡
                      })
                with open('data.json', 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                
                time.sleep(0.05)  # 等待50毫秒
                
    except KeyboardInterrupt:  # 当按下 Ctrl + \ 时触发 KeyboardInterrupt 异常
        print("\n停止数据采集")
        collecting_data = False

uartGetTLVdata("PMB")

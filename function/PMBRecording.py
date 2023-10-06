import serial
from mmWave import peopleMB
import datetime
import json
import time





class GlobalV:
    count = 0
    def __init__(self, count):
        self.count = count

class UartGetTLVdata:
    def __init__(self, name, port, pause_point):
        self.name = name
        self.port = port
        self.pause_point = pause_point
        self.gv = GlobalV(0)
        self.pm = peopleMB.PeopleMB(port)

    def v6Unpack(self, v6Data):
        print("---v6解包---")

    def v7UnpackXY(self, v7Data):
        print("---v7解包---")
        v7xy = []
        for k in v7Data:
            v7xy.append({"位置X": k[1], "位置Y": k[2]})   
        return v7xy

    def v7UnpackVelocityXY(self, v7Data): # 速度 X, Y
        velxy = []
        for k in v7Data:
            velxy.append({"速度X": k[3], "速度Y": k[4]})
        return velxy

    def run(self):
        data = {
            "數據": [],
            "TLV數量": {
                "v6": 0,
                "v7": 0,
                "v8": 0
            }
        }
        with open(f'out/{self.name}.json', 'w', encoding='utf-8') as json_file:
            json.dump({}, json_file, ensure_ascii=False)

        print("mmWave:人員移動行為 {:} 示例:".format(self.name))
        pt = datetime.datetime.now()
        ct = datetime.datetime.now()
        self.port.flushInput()
        self.pm.useDebug(True)

        collecting_data = True  # 添加一個標誌變量来控制數據采集

        try:
            count = 0
            while collecting_data:
                ct = datetime.datetime.now()
                (dck, v6, v7, v8) = self.pm.tlvRead(False)
                hdr = self.pm.getHeader()
                if dck:
                    print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})] {}\n".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8),ct-pt))
                    pt = ct
                    xy = self.v7UnpackXY(v7)
                    print("位置[X,Y]:",xy)
                    vxy = self.v7UnpackVelocityXY(v7)
                    print("速度[X,Y]:",vxy)
                    # 更新TLV數量
                    data["TLV數量"]["v6"] = len(v6)
                    data["TLV數量"]["v7"] = len(v7)
                    data["TLV數量"]["v8"] = len(v8)
                    #print(f"v6 length: {len(v6)}, v7 length: {len(v7)}, v8 length: {len(v8)}")
                        
                    with open(f'out/{self.name}.json', 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        timestamp = ct.strftime("%Y-%m-%d %H:%M:%S.%f")
                        if "數據" not in data:
                            data["數據"] = []
                        if "TLV數量" not in data:
                            data["TLV數量"] = {"v6": 0, "v7": 0, "v8": 0}
                            data["TLV數量"]["v6"] = len(v6)
                            data["TLV數量"]["v7"] = len(v7)
                            data["TLV數量"]["v8"] = len(v8)
                        data["數據"].append({"檢測數": hdr.frameNumber, "時間軸": timestamp, "位置": xy, "速度": vxy,"v6數量": len(v6),  # 修正這裡
                        "v7數量": len(v7),  "v8數量": len(v8)    })

                    with open(f'out/{self.name}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(data, json_file, ensure_ascii=False, indent=4)

                    time.sleep(0.05)  # 等待50毫秒
                count+=1
                if count >= self.pause_point:
                    print("\n到達自定義暫停點")
                    collecting_data = False
                
        except KeyboardInterrupt:  # 當按下 Ctrl + \ 時觸發 KeyboardInterrupt 異常
            print("\n停止數據采集")
            collecting_data = False

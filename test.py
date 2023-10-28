import RPi.GPIO as GPIO
import time
import threading
import os

class LEDController:
    blink_flag=0 # 閃爍flag

    def __init__(self, Config):
        # 從設定檔中取得LED的GPIO針腳
        self.red_pin = self.get_pins(Config['LED']['red_pin'])
        self.orange_pin = self.get_pins(Config['LED']['orange_pin'])
        self.green_pin = self.get_pins(Config['LED']['green_pin'])

        # 將所有的GPIO針腳放入一個列表中
        self.all_pins = self.red_pin+self.orange_pin+self.green_pin

        # 從設定檔中取得GPIO模式
        self.mode = GPIO.BCM if Config['LED']['mode'] == 'GPIO.BCM' else GPIO.BOARD
        # 從設定檔中取得閃爍間隔和次數
        self.interval= Config['LED']['interval']
        self.blink_time= Config['LED']['blink_time']
        
        # 設置GPIO模式為BCM或BOARD
        GPIO.setmode(self.mode)

        # 設置LED針腳為輸出模式
        for pin in self.all_pins:
            GPIO.setup(pin, GPIO.OUT)

    def get_pins(self, pin_config):
        # 將設定檔中的GPIO針腳轉換為整數列表
        if isinstance(pin_config, str):
            return list(map(int, pin_config.split(',')))
        else:
            return [int(pin_config)]
            
    def turn_off(self, pins):
        # 關閉指定的GPIO針腳
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)

    def turn_on(self, pins):
        # 打開指定的GPIO針腳
        for pin in pins:
            GPIO.output(pin, GPIO.HIGH)

    def blink(self, pins, times=3):#pin:腳位，times:閃爍次數
        if self.blink_flag == 1:
            return 5 #等待
        self.blink_flag = 1

        count = times
        while True:
            count = self.blink_unit(pins, count)
            if count == 0:
                self.blink_flag = 0
                return 1 #正常結束

    def blink_unit(self, pins, counts):
        # 閃爍指定的GPIO針腳
        self.turn_on(pins)
        time.sleep(self.interval)
        self.turn_off(pins)
        time.sleep(self.interval)
        return counts-1
    
if __name__ == "__main__":
    os.chdir("/home/led/project/Basic-experimental-framework")
    from function.ConfigLoader import ConfigLoader
    System_config_dir = 'config' # 設定config目錄，會自動讀取全部檔案
    System_config_data = ConfigLoader(System_config_dir).config_dict

    # 創建一個LEDController物件
    led_controller = LEDController(System_config_data)
    
    # 閃爍紅色LED燈
    led_controller.blink(led_controller.red_pin, times=3)
    
    # 等待一秒
    time.sleep(1)
    
    # 閃爍橙色LED燈
    led_controller.blink(led_controller.orange_pin, times=3)
    
    # 等待一秒
    time.sleep(1)
    
    # 閃爍綠色LED燈
    led_controller.blink(led_controller.green_pin, times=3)

    # 閃爍全部LED燈
    led_controller.blink(led_controller.all_pins, times=3)

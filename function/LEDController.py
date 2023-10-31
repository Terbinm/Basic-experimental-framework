import RPi.GPIO as GPIO
import time,os
import threading
import configparser

class LEDController:
    blink_flag=0 #閃爍flag
    def __init__(self, Config):
        self.red_pin = self.get_pins(Config['LED']['red_pin'])
        self.orange_pin = self.get_pins(Config['LED']['orange_pin'])
        self.green_pin = self.get_pins(Config['LED']['green_pin'])

        self.all_pins = self.red_pin+self.orange_pin+self.green_pin

        self.mode = GPIO.BCM if Config['LED']['mode'] == 'GPIO.BCM' else GPIO.BOARD
        self.interval= Config['LED']['interval']
        self.blink_time= Config['LED']['blink_time']
        
        # 設置GPIO模式為BCM
        GPIO.setmode(self.mode)
        # 設置LED針腳為輸出模式
        for pin in self.all_pins:
            GPIO.setup(pin, GPIO.OUT)

        
    def get_pins(self, pin_config):
        if isinstance(pin_config, str):
            return list(map(int, pin_config.split(',')))
        else:
            return [int(pin_config)]
    
    # def __init__(self, led_pins=[2, 3, 4], mode=GPIO.BCM,interval =0.5):
        
    #     self.led_pins = Config['LED']['led_pins']
    #     # 設置GPIO模式為BCM
    #     GPIO.setmode(mode)
    #     # 定義LED的GPIO針腳
    #     self.led_pins = led_pins
    #     # 設置LED針腳為輸出模式
    #     for pin in self.led_pins:
    #         GPIO.setup(pin, GPIO.OUT)

            
    #     self.interval = interval

    def turn_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

    def turn_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def blink(self, pin, blink_time=None):#pin:腳位，times:閃爍次數
        if self.blink_flag == 1:
            return 5 #等待
        self.blink_flag = 1

        if blink_time:
            count = self.blink_time
        else:
            count = blink_time

        while True:
            count = self.blink_unit(pin, count)
            if count == 0:
                self.blink_flag = 0
                return 1 #正常結束

    def blink_unit(self, pin, counts):
        self.turn_on(pin)
        time.sleep(self.interval)
        self.turn_off(pin)
        time.sleep(self.interval)
        return counts-1
    
if __name__ == "__main__":
    # GPIO.cleanup(2)  # 清除針腳設置
    # GPIO.cleanup(3)  # 清除針腳設置
    # GPIO.cleanup(4)  # 清除針腳設置
    os.chdir("/home/led/project/Basic-experimental-framework")
    from ConfigLoader import ConfigLoader
    System_config_dir = 'config' # 設定config目錄，會自動讀取全部檔案
    System_config_data = ConfigLoader(System_config_dir).config_dict
    led_controller = LEDController(System_config_data)

    # # 打開 GPIO 針腳 2 的 LED
    # led_controller.turn_on(2)
    # time.sleep(1)  # 等待一秒

    # # 關閉 GPIO 針腳 2 的 LED
    # led_controller.turn_off(2)
    # time.sleep(1)  # 等待一秒

    # 讓 GPIO 針腳 3 的 LED 閃爍三次
    led_controller.blink(2, led_controller.blink_time)
    # 讓 GPIO 針腳 3 的 LED 閃爍三次
    led_controller.blink(3, led_controller.blink_time)
    # 讓 GPIO 針腳 3 的 LED 閃爍三次
    led_controller.blink(4, led_controller.blink_time)
    
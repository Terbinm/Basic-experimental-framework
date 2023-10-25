import RPi.GPIO as GPIO
import time
import threading
class LEDController:
    blink_flag=0 #閃爍flag
    def __init__(self, led_pins=[2, 3, 4], mode=GPIO.BCM,interval =0.5):
        
        # 設置GPIO模式為BCM
        GPIO.setmode(mode)
        # 定義LED的GPIO針腳
        self.led_pins = led_pins
        # 設置LED針腳為輸出模式
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)

            
        self.interval = interval

    def turn_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

    def turn_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def blink(self, pin, times=3):#pin:腳位，times:閃爍次數
        if self.blink_flag == 1:
            return 5 #等待
        
        self.blink_flag = 1
        count = times
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
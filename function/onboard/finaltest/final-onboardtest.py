import RPi.GPIO as GPIO
import time
import threading
"""
# 設置GPIO模式為BCM
GPIO.setmode(GPIO.BCM)

# 定義按鈕和LED的GPIO針腳
button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
led_pins = [2, 3, 4]  # 三個LED的GPIO針腳
"""

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

class ButtonController:
    def __init__(self, button_pins=[17, 27, 22], led_controller=None, mode=GPIO.BCM, pud=GPIO.PUD_UP, event=GPIO.FALLING, bouncetime=500):
        # 設置GPIO模式為BCM
        GPIO.setmode(mode)

        # 定義按鈕的GPIO針腳
        self.button_pins = button_pins

        # 設置按鈕針腳為輸入模式，並啟用內部上拉電阻
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

        # 為每個按鈕設置事件偵測和回調函數
        for pin in self.button_pins:
            GPIO.add_event_detect(pin, event, callback=self.button_callback, bouncetime=bouncetime) #多線程

            # GPIO.add_event_detect(pin, event, callback=self.handle_button, bouncetime=bouncetime) #單線程

        # LED控制器
        self.led_controller = led_controller

    def button_callback(self, channel):
        # 創建一個新的線程來執行回調函數
        thread = threading.Thread(target=self.handle_button, args=(channel,))
        thread.start()

    def handle_button(self, channel):
        print("關閉LED燈")
        if channel == self.button_pins[0]: ##按鈕功能0
            print("關閉LED燈")
            for pin in self.led_controller.led_pins:
                self.led_controller.turn_off(pin)

        elif channel == self.button_pins[1]: ##按鈕功能1
            print("開啟LED燈")
            for pin in self.led_controller.led_pins:
                self.led_controller.turn_on(pin)

        elif channel == self.button_pins[2]: ##按鈕功能2
            print("LED燈閃爍")
            for pin in self.led_controller.led_pins:
                self.led_controller.blink(pin,5)

    def run(self):
        # 主迴圈，讓程式保持運行
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()

# 使用範例
led_controller = LEDController()
button_controller = ButtonController(led_controller=led_controller)
button_controller.run()

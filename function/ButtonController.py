import RPi.GPIO as GPIO
import time
import threading
class ButtonController:
    def __init__(self, button_pins=[17, 27, 22], button_functions=[], led_controller=None, mode=GPIO.BCM, pud=GPIO.PUD_UP, event=GPIO.FALLING, bouncetime=500):
        # 設置GPIO模式為BCM
        GPIO.setmode(mode)

        # 定義按鈕的GPIO針腳
        self.button_pins = button_pins

        # 將每個按鈕與其對應的功能關聯起來
        self.button_functions = dict(zip(button_pins, button_functions))

        # 設置按鈕針腳為輸入模式，並啟用內部上拉電阻
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

        # 為每個按鈕設置事件偵測和回調函數
        for pin in self.button_pins:
            GPIO.add_event_detect(pin, event, callback=self.button_callback, bouncetime=bouncetime)

        # LED控制器
        self.led_controller = led_controller

    def button_callback(self, channel):
        # 創建一個新的線程來執行回調函數
        thread = threading.Thread(target=self.button_functions[channel], args=(channel,))
        thread.start()

    def run(self):
        # 主迴圈，讓程式保持運行
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()
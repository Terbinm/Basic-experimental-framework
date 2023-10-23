import RPi.GPIO as GPIO
import time
import threading

class ButtonController:
    def __init__(self, button_pins=[17, 27, 22], mode=GPIO.BCM, pud=GPIO.PUD_UP, event=GPIO.FALLING, bouncetime=500):
        # 設置GPIO模式為BCM
        GPIO.setmode(mode)

        # 定義按鈕的GPIO針腳
        self.button_pins = button_pins

        # 設置按鈕針腳為輸入模式，並啟用內部上拉電阻
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

        # 為每個按鈕設置事件偵測和回調函數
        for pin in self.button_pins:
            GPIO.add_event_detect(pin, event, callback=self.button_callback, bouncetime=bouncetime)

    def button_callback(self, channel):
        # 創建一個新的線程來執行回調函數
        thread = threading.Thread(target=self.handle_button, args=(channel,))
        thread.start()

    def handle_button(self, channel):
        if channel == self.button_pins[0]: ##按鈕功能0
            print("flag: "+str(self.flag))

        elif channel == self.button_pins[1]: ##按鈕功能1
            print("LED燈閃爍！")

        elif channel == self.button_pins[2]: ##按鈕功能2
            print("開始5秒計時器！")
            self.flag = 1
            time.sleep(5)
            print("計時器結束！")
            self.flag = 0

    def run(self):
        # 主迴圈，讓程式保持運行
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()

# 使用範例
controller = ButtonController(button_pins=[17, 27, 22],bouncetime=500)
controller.run()

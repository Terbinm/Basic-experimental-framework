import RPi.GPIO as GPIO
import time
import threading
class ButtonController:
    def __init__(self, Config, button_functions=[], led_controller=None):
        # 從設定檔中取得按鈕的GPIO針腳和相關設定
        self.button_pins = self.get_pins(Config['Button']['button_pins'])
        
        # 將每個按鈕與其對應的功能關聯起來
        self.button_functions = dict(zip(self.button_pins, button_functions))

        self.mode = GPIO.BCM if Config['Button']['mode'] == 'GPIO.BCM' else GPIO.BOARD
        self.pud = GPIO.PUD_UP if Config['Button']['pud'] == 'GPIO.PUD_UP' else GPIO.PUD_DOWN
        self.event = GPIO.FALLING if Config['Button']['event'] == 'GPIO.FALLING' else GPIO.RISING
        self.bouncetime = Config['Button']['bouncetime']

        GPIO.setmode(self.mode)

        # 設置按鈕針腳為輸入模式，並啟用內部上拉電阻
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=self.pud)

        # 為每個按鈕設置事件偵測和回調函數
        for pin in self.button_pins:
            GPIO.add_event_detect(pin, self.event, callback=self.button_callback, bouncetime=self.bouncetime)

        # LED控制器
        self.led_controller = led_controller
        
    def get_pins(self, pin_config):
        if isinstance(pin_config, str):
            return list(map(int, pin_config.split(',')))
        else:
            return [int(pin_config)]
        
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



import RPi.GPIO as GPIO
import time

class ButtonDetector:
    def __init__(self, pin):
        self.pin = pin
        self.button_pressed = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def button_callback(self):
        if not self.button_pressed:
            self.button_pressed = False
            print("Button pressed!")
        else:
            self.button_pressed = True

# 使用範例
detector = ButtonDetector(22)
while True:
    time.sleep(10)
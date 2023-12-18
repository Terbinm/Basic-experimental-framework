import RPi.GPIO as GPIO
import time

# 設定GPIO模式
GPIO.setmode(GPIO.BCM)

# 定義LED和按鈕的GPIO
leds = [13, 19, 26]
buttons = [17, 27, 22]

# 設定LED輸出和按鈕輸入
for led in leds:
    GPIO.setup(led, GPIO.OUT)
for button in buttons:
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        for button, led in zip(buttons, leds):
            if GPIO.input(button) == GPIO.LOW:
                GPIO.output(led, GPIO.HIGH)
            else:
                GPIO.output(led, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

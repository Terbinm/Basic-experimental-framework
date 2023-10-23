import RPi.GPIO as GPIO

from function.ButtonMonitorBasic import ButtonMonitor


# 設置GPIO模式為BCM
GPIO.setmode(GPIO.BCM)

# 定義按鈕和LED的GPIO針腳
button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
led_pins = [2, 3, 4]  # 三個LED的GPIO針腳


monitor = ButtonMonitor(button_pins, led_pins)
monitor.start()

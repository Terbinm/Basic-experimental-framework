import RPi.GPIO as GPIO

from function.ButtonMonitor import ButtonMonitor


# 設置GPIO模式為BCM
GPIO.setmode(GPIO.BCM)

# 定義按鈕和LED的GPIO針腳
button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
led_pins = [2, 3, 4]  # 三個LED的GPIO針腳


# monitor = ButtonMonitor(button_pins, led_pins)
# monitor.start()

# 定義每個按鈕要執行的動作
def do_somethingA():
    index= 0

def do_somethingB():
    index= 1

def do_somethingC():
    index= 2

actions = [do_somethingA, do_somethingB, do_somethingC]
# 建立ButtonController物件
ButtonController = [ButtonMonitor(pin, action) for pin, action in zip(button_pins, actions)]
ButtonController[0].start()
ButtonController[1].start()
ButtonController[2].start()
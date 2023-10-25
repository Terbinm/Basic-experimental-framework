import RPi.GPIO as GPIO
import time
import threading

from function.ButtonController import ButtonController
from function.LEDController import LEDController
"""
# 設置GPIO模式為BCM
GPIO.setmode(GPIO.BCM)

# 定義按鈕和LED的GPIO針腳
button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
led_pins = [2, 3, 4]  # 三個LED的GPIO針腳
"""





###############################################################

# 創建LED控制器
led_controller = LEDController()

# 定義按鈕的功能
def turn_off_leds(channel):
    print("關閉LED燈")
    for pin in led_controller.led_pins:
        led_controller.turn_off(pin)

def turn_on_leds(channel):
    print("開啟LED燈")
    for pin in led_controller.led_pins:
        led_controller.turn_on(pin)

def blink_leds(channel):
    print("LED燈閃爍")
    for pin in led_controller.led_pins:
        led_controller.blink(pin,5) 


# 創建按鈕控制器，並將按鈕的功能作為參數傳遞
button_functions = [turn_off_leds, turn_on_leds, blink_leds]
button_controller = ButtonController(button_functions=button_functions, led_controller=led_controller) #onboard處理
thread = threading.Thread(target=button_controller.run, args=())
thread.start()
# 運行按鈕控制器

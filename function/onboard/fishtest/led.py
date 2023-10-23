import RPi.GPIO as GPIO
import time

# 設置GPIO模式為BCM
GPIO.setmode(GPIO.BCM)

# 定義按鈕和LED的GPIO針腳
button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
led_pins = [2, 3, 4]  # 三個LED的GPIO針腳

# 設置GPIO針腳狀態
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# 定義函數來控制LED
def control_led(led_pin):
    led_state = GPIO.input(led_pin)
    GPIO.output(led_pin, not led_state)

try:
    while True:
        for i, button_pin in enumerate(button_pins):
            # 監聽按鈕狀態
            button_state = GPIO.input(button_pin)
            print("監聽中...")
            
            # 如果按鈕被按下，切換相應的LED狀態
            if button_state == GPIO.HIGH:
                control_led(led_pins[i])
                print("按按鈕")

        time.sleep(0.3)  # 避免快速多次觸發按鈕

except KeyboardInterrupt:
    GPIO.cleanup()

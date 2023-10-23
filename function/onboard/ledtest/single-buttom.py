import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.button_callback, bouncetime=20)

    def button_callback(self, channel):
        print("Button was pushed!")

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    button = Button(22)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        button.cleanup()

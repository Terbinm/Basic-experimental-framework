import RPi.GPIO as GPIO
import time
import threading


class ButtonMonitor:
    def __init__(self, button_pins, thread):
        self.button_pins = button_pins
        self.running = False
        self.thread = thread

        
        # 設置GPIO針腳狀態
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN)


    def _monitor(self):
        while self.running:
            for i in range(len(self.button_pins)):
                if GPIO.input(self.button_pins[i]) == GPIO.HIGH:
                    print(f"Button {i} pressed")
                    
                else:
                    pass
            time.sleep(0.05)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()

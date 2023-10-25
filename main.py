
import RPi.GPIO as GPIO
import time
import threading
from function.BasicServerConnect import BasicServerConnect
from function.ThreadingRecording import AudioExperiment
from function.DataSaver import DataSaver
from function.ConfigLoader import ConfigLoader
from function.ButtonController import ButtonController
from function.LEDController import LEDController
import time,os
"""
# 設置GPIO模式為BCM
GPIO.setmode(GPIO.BCM)

# 定義按鈕和LED的GPIO針腳
button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
led_pins = [2, 3, 4]  # 三個LED的GPIO針腳
"""
###############################################################
#設定路徑(程式執行的路徑)
os.chdir("/home/led/project/Basic-experimental-framework")
config_dir = 'config' # 設定config目錄，會自動讀取全部檔案
edgeID = 'Sound1' #裝置編號
###############################################################

# 創建LED控制器
led_controller = LEDController()

# 定義按鈕的功能
def turn_off_leds(channel):#啟動錄音
    print("啟動錄音")
    #TODO(LED): 實驗任務調度器
    #開始錄音實驗
    Audio_Experiment = AudioExperiment(config_data) #初始化 實驗物件
    Audio_Experiment.run_experiment() #執行實驗

    #TODO(LED): 統一調度
    while Audio_Experiment.get_is_handle_finish() is False: #等待實驗完成
        time.sleep(0.1)  # 暫停1秒

    data_saver.save_data_to_json(
        Audio_Experiment.get_handle_results(),
        config_data['path']['output_data_filename'])#儲存實驗結果
    uploader = BasicServerConnect(edgeID, data_saver.dir_path)  # 建立一個FileUploader實例
    uploader.upload_files()  
    print("finish")

def turn_on_leds(channel):#強制暫停(TODO)
    print("開啟LED燈")
    for pin in led_controller.led_pins:
        led_controller.turn_on(pin)

def blink_leds(channel):#無功能，暫時為重設LED燈(好像沒用(X))
    print("關閉LED燈")
    for pin in led_controller.led_pins:
        led_controller.turn_off(pin)

#讀取config
config_data = ConfigLoader(config_dir).config_dict

#創造資料夾並儲存
data_saver = DataSaver(config_data) #初始化 儲存器物件
config_data['path']['output_dir-final'] = data_saver.dir_path #設定資料夾

# 創建按鈕控制器，並將按鈕的功能作為參數傳遞
button_functions = [turn_off_leds, turn_on_leds, blink_leds]
button_controller = ButtonController(button_functions=button_functions, led_controller=led_controller) #onboard處理
thread = threading.Thread(target=button_controller.run, args=())
# 運行按鈕控制器


thread.start() #原...程式，啟動！

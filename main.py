
from function.BasicServerConnect import BasicServerConnect, FileUploader
from function.ThreadingRecording import AudioExperiment #多線程實驗執行器
from function.DataSaver import DataSaver #資料儲存
from function.ConfigLoader import ConfigLoader #config載入器
from function.ButtonController import ButtonController #按鈕控制器
from function.LEDController import LEDController #LED控制器
from function.controler import Experiment #統一實驗調度器
import time, os, logging
import threading
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
edgeID = 'Soundtest_ModelA' #裝置編號 #不需設定，已廢棄
logging.basicConfig(filename=os.path.join('out','Running.log'), level=logging.DEBUG)#log設定
###############################################################


#讀取config
system_config_data = ConfigLoader(config_dir).config_dict
# 創建LED控制器
led_controller = LEDController(system_config_data)

# 創建網路連線
Send_State = BasicServerConnect(system_config_data) 
# 定義按鈕的功能
def DoEx(channel):#啟動實驗
    try:
        for pin in led_controller.all_pins:
            led_controller.turn_off(pin)
        led_controller.turn_on(led_controller.orange_pin)
        Send_State.send_status("waiting_for_prepare")

        DoEx_config_dir = 'config/DoEx'
        config_data = ConfigLoader(DoEx_config_dir).config_dict

        data_saver = DataSaver(config_data)
        config_data['path']['output_dir-final'] = data_saver.dir_path

        Send_State.send_status("Starting_Ex")
        Audio_Experiment = AudioExperiment(config_data)
        Audio_Experiment.run_experiment()

        # while Audio_Experiment.get_is_handle_finish() is False:
        #     time.sleep(0.1)

        data_saver.save_data_to_json(
        Audio_Experiment.get_handle_results(),
        config_data['path']['output_data_filename'])
        Send_State.send_status("Finish_Ex: "+str(data_saver.dir_path))
    except Exception as e:
        print(f"Error DoEx:{e}")
        for pin in led_controller.all_pins:
            led_controller.turn_off(pin)
        led_controller.blink(led_controller.red_pin,3)
        return 4
    
        
    # #file upload
    try:
        uploader = FileUploader(system_config_data, data_saver.dir_path)
        uploader.upload_files()
        Send_State.send_status("finish_upload_files")
        logging.info('DoEx: finish_upload_files')
    except Exception as e:
        logging.error(f"Error uploading files: {e}")
        print(f"Error uploading files:{e}")
        return 4

    led_controller.turn_off(led_controller.orange_pin)
    led_controller.blink(led_controller.green_pin,3)

    return 1

def turn_on_leds(channel):#強制暫停(TODO)
    print("開啟LED燈")
    for pin in led_controller.all_pins:
        led_controller.turn_on(pin)
    return 1

def turn_off_leds(channel):#無功能，暫時為重設LED燈(好像沒用(X))
    print("關閉LED燈")
    for pin in led_controller.all_pins:
        led_controller.turn_off(pin)
    return 1



# #創造資料夾並儲存
# data_saver = DataSaver(config_data) #初始化 儲存器物件
# config_data['path']['output_dir-final'] = data_saver.dir_path #設定資料夾

# 創建按鈕控制器，並將按鈕的功能作為參數傳遞
button_functions = [DoEx, turn_on_leds, turn_off_leds]
button_controller = ButtonController(system_config_data,button_functions=button_functions, led_controller=led_controller) #onboard處理
thread = threading.Thread(target=button_controller.run, args=())
# 運行按鈕控制器


Send_State.send_status("Online") 
thread.start() #原...程式，啟動！

import time,os,logging


from function.BasicServerConnect import BasicServerConnect,FileUploader #伺服器上傳/連接
from function.ConfigLoader import ConfigLoader
from function.DataSaver import DataSaver
from function.ThreadingRecording import AudioExperiment

#設定路徑(程式執行的路徑)#外部應該回傳的參數
os.chdir("/home/led/project/Basic-experimental-framework")
#讀取config(系統)
System_config_dir = 'config' # 設定config目錄，會自動讀取全部檔案
System_config_data = ConfigLoader(System_config_dir).config_dict
logging.basicConfig(filename=os.path.join('out','Running.log'), level=logging.DEBUG) # log記錄器
#########################################
# 狀態值說明(按發生順序排序)
# waiting_for_prepare  #等待系統準備所有資源
# Starting_Ex          #開始實驗
# Finish_Ex            #完成實驗     (已完成，但需要手動上傳檔案)
# finish_upload_files  #檔案上傳完畢  (完美完成)

# ExError_for_XXX      #發生錯誤(xxx為說明)


#開始單次實驗
try:
    Send_State = BasicServerConnect(System_config_data)  # 建立一個FileUploader實例
    Send_State.send_status("waiting_for_prepare")
    logging.info('DoEx: waiting for prepare')
except Exception as e:
    logging.error(f"DoEx: Error starting experiment-{e}")
    print(f"DoEx: Error starting experiment-{e}")


#下載connfig(實驗用)(未來要做)TODO

#讀取config(實驗用)
try:
    config_dir = 'config/DoEx' # 設定config目錄，會自動讀取全部檔案
    config_data = ConfigLoader(config_dir).config_dict
    logging.info('DoEx: Config loaded')
except Exception as e:
    logging.error(f"DoEx: Error loading experiment config-{e}")
    print(f"DoEx: Error loading experiment config-{e}")

#創造資料夾並儲存
try:
    data_saver = DataSaver(config_data) #初始化 儲存器物件
    config_data['path']['output_dir-final'] = data_saver.dir_path #設定資料夾
    logging.info('DoEx: path created')
except Exception as e:
    logging.error(f"DoEx: Error creating path-{e}")
    print(f"DoEx: Error creating path-{e}")

#TODO(LED): 實驗任務調度器
#開始錄音實驗
try:
    logging.info('DoEx: Starting_Ex')
    Send_State.send_status("Starting_Ex")
    Audio_Experiment = AudioExperiment(config_data) #初始化 實驗物件
    Audio_Experiment.run_experiment() #執行實驗
except Exception as e:
    logging.error(f"DoEx: Error starting audio experiment-{e}")
    print(f"DoEx: Error starting audio experiment-{e}")

#TODO(LED): 統一調度
#等待實驗完成
try:
    while Audio_Experiment.get_is_handle_finish() is False: #等待實驗完成
        time.sleep(0.1)  # 暫停1秒
except Exception as e:
    logging.error(f"DoEx:Error during audio experiment-{e}")
    print(f"DoEx:Error during audio experiment-{e}")
   
#儲存結果到檔案 
try:
    data_saver.save_data_to_json(
        Audio_Experiment.get_handle_results(),
        config_data['path']['output_data_filename'])#儲存實驗結果
    Send_State.send_status("Finish_Ex")
    logging.info('DoEx: Finish_Ex')
except Exception as e:
    logging.error(f"Error saving experiment results: {e}")
    print(f"Error saving experiment results: {e}")

# 實驗完成，上傳檔案
try:
    uploader = FileUploader(System_config_data, data_saver.dir_path) # 建立一個FileUploader實例
    uploader.upload_files()# 上傳所有檔案
    Send_State.send_status("finish_upload_files")
    logging.info('DoEx: finish_upload_files')
except Exception as e:
    logging.error(f"Error uploading files: {e}")
    print(f"Error uploading files:{e}")
    

logging.info('DoEx: finish_Ex')


#開始MMwave實驗
# from function.ThreadingMMwave import MMwaveExperiment
# MMwave_Experiment = MMwaveExperiment(config_data) #初始化 實驗物件
# MMwave_Experiment.run_experiment() #執行實驗

# while MMwave_Experiment.get_is_handle_finish() is False: #等待實驗完成
#     time.sleep(0.1)  # 暫停1秒
# data_saver.save_data_to_json(MMwave_Experiment.get_handle_results(),config_data['path']['output_data_filename'])#儲存實驗結果
# print("finish")

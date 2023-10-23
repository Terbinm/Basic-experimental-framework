import time,os

#設定路徑(程式執行的路徑)
os.chdir("/home/led/project/Basic-experimental-framework")

#讀取config
config_dir = 'config' # 設定config目錄，會自動讀取全部檔案

from ConfigLoader import ConfigLoader
config_data = ConfigLoader(config_dir).config_dict


#創造資料夾並儲存
from DataSaver import DataSaver
data_saver = DataSaver(config_data) #初始化 儲存器物件
config_data['path']['output_dir-final'] = data_saver.dir_path #設定資料夾



#TODO(LED): 實驗任務調度器
#開始錄音實驗
from ThreadingRecording import AudioExperiment
Audio_Experiment = AudioExperiment(config_data) #初始化 實驗物件
Audio_Experiment.run_experiment() #執行實驗

#TODO(LED): 統一調度
while Audio_Experiment.get_is_handle_finish() is False: #等待實驗完成
    time.sleep(0.1)  # 暫停1秒
data_saver.save_data_to_json(
    Audio_Experiment.get_handle_results(),
    config_data['path']['output_data_filename'])#儲存實驗結果
print("finish")


#開始MMwave實驗
# from ThreadingMMwave import MMwaveExperiment
# MMwave_Experiment = MMwaveExperiment(config_data) #初始化 實驗物件
# MMwave_Experiment.run_experiment() #執行實驗

# while MMwave_Experiment.get_is_handle_finish() is False: #等待實驗完成
#     time.sleep(0.1)  # 暫停1秒
# data_saver.save_data_to_json(MMwave_Experiment.get_handle_results(),config_data['path']['output_data_filename'])#儲存實驗結果
# print("finish")

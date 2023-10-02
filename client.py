import time

#讀取config
from function.ConfigLoader import ConfigLoader
config_data = ConfigLoader('config').config_dict

#創造資料夾並儲存
from function.DataSaver import DataSaver
data_saver = DataSaver(config_data) #初始化 儲存器物件
path = data_saver.save(config_data,"config") #初始化資料夾
print(data_saver.get_dir_path())

#開始錄音實驗
from function.ThreadingRecording import AudioExperiment
Audio_Experiment = AudioExperiment(config_data) #初始化 實驗物件
Experiment_Sound = Audio_Experiment.run_experiment() #執行實驗


while Audio_Experiment.get_is_handle_finish() is False: #等待實驗完成
    time.sleep(0.1)  # 暫停1秒
data_saver.save_data_to_json(Audio_Experiment.get_handle_results(),"Audio_results")#儲存實驗結果
print("finish")

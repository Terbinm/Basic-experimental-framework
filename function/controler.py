import time, os, logging
from function.BasicServerConnect import BasicServerConnect, FileUploader
from function.ConfigLoader import ConfigLoader
from function.DataSaver import DataSaver
from function.ThreadingRecording import AudioExperiment

class Experiment:
    def __init__(self,System_config_data):
        # 初始化實驗環境
        self.System_config_data = System_config_data
        #設定實驗倉
        self.function_dict = {0: self.run_AIM,
                              1: self.run_recording,
                              2: self.run_mmwave,
                              3: self.run_Cam}
        
    def start_experiment(self):
        # 開始實驗
        try:
            self.Send_State = BasicServerConnect(self.System_config_data)
            self.Send_State.send_status("waiting_for_prepare")
            logging.info('DoEx: waiting for prepare')
        except Exception as e:
            logging.error(f"DoEx: Error starting experiment-{e}")
            print(f"DoEx: Error starting experiment-{e}")

    def load_config(self):
        # 讀取實驗設定
        try:
            config_dir = 'config/DoEx'
            self.config_data = ConfigLoader(config_dir).config_dict
            logging.info('DoEx: Config loaded')
        except Exception as e:
            logging.error(f"DoEx: Error loading experiment config-{e}")
            print(f"DoEx: Error loading experiment config-{e}")

    def create_path(self):
        # 創建資料儲存路徑
        try:
            self.data_saver = DataSaver(self.config_data)
            self.config_data['path']['output_dir-final'] = self.data_saver.dir_path
            logging.info('DoEx: path created')
        except Exception as e:
            logging.error(f"DoEx: Error creating path-{e}")
            print(f"DoEx: Error creating path-{e}")

    def run_audio_experiment(self):
        # 開始錄音實驗
        try:
            logging.info('DoEx: Starting_Ex')
            self.Send_State.send_status("Starting_Ex")
            self.Audio_Experiment = AudioExperiment(self.config_data)
            self.Audio_Experiment.run_experiment()
        except Exception as e:
            logging.error(f"DoEx: Error starting audio experiment-{e}")
            print(f"DoEx: Error starting audio experiment-{e}")

    def wait_for_completion(self):
        # 等待實驗完成
        try:
            while self.Audio_Experiment.get_is_handle_finish() is False:
                time.sleep(0.1)
        except Exception as e:
            logging.error(f"DoEx:Error during audio experiment-{e}")
            print(f"DoEx:Error during audio experiment-{e}")

    def save_results(self):
        # 儲存實驗結果
        try:
            self.data_saver.save_data_to_json(
            self.Audio_Experiment.get_handle_results(),
            self.config_data['path']['output_data_filename'])
            self.Send_State.send_status("Finish_Ex")
            logging.info('DoEx: Finish_Ex')
            return 1
        except Exception as e:
            logging.error(f"Error saving experiment results: {e}")
            print(f"Error saving experiment results: {e}")

    def upload_files(self):
        # 上傳檔案
        try:
            uploader = FileUploader(self.System_config_data, self.data_saver.dir_path)
            uploader.upload_files()
            self.Send_State.send_status("finish_upload_files")
            logging.info('DoEx: finish_upload_files')
        except Exception as e:
            logging.error(f"Error uploading files: {e}")
            print(f"Error uploading files:{e}")

    def run_AIM(self):
        # 一次執行錄音實驗
        print("啟動錄音")
        self.run_audio_experiment()
        self.wait_for_completion()
        self.save_results()
        self.upload_files()
        
    def run_recording(self):
        # 一次執行錄音實驗
        print("啟動錄音")
        self.run_audio_experiment()
        self.wait_for_completion()
        self.save_results()
        self.upload_files()

    def run_mmwave(self):
        pass
    def run_Cam(self):
        pass

    def Match_Ex(self):
        self.start_experiment()
        if self.load_config():
            self.create_path()
            edge_type = self.config_data['edge']['edge_type']
            
            if edge_type in self.function_dict:
                self.function_dict[edge_type]()
            else:
                print("Invalid edge_type")
                return 1


if __name__ == "__main__":
    os.chdir("/home/led/project/Basic-experimental-framework")
    logging.basicConfig(filename=os.path.join('out','Running.log'), level=logging.DEBUG)
    System_config_dir = 'config'
    System_config_data = ConfigLoader(System_config_dir).config_dict


    #真正執行的地方
    ex = Experiment(System_config_data,)
    ex.Match_Ex()

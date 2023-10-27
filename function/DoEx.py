import time, os, logging

from BasicServerConnect import BasicServerConnect, FileUploader  # 伺服器上傳/連接
from ConfigLoader import ConfigLoader
from DataSaver import DataSaver
from ThreadingRecording import AudioExperiment

class Experiment:
    def __init__(self):
        # 設定路徑(程式執行的路徑)
        os.chdir("/home/led/project/Basic-experimental-framework")
        # 讀取config(系統)
        System_config_dir = 'config'  # 設定config目錄，會自動讀取全部檔案
        self.System_config_data = ConfigLoader(System_config_dir).config_dict
        logging.basicConfig(filename=os.path.join('out', 'Running.log'), level=logging.DEBUG)  # log記錄器

    def start_experiment(self):
        try:
            self.Send_State = BasicServerConnect(self.System_config_data)  # 建立一個FileUploader實例
            self.Send_State.send_status("waiting_for_prepare")
            logging.info('DoEx: waiting for prepare')
        except Exception as e:
            logging.error(f"DoEx: Error starting experiment-{e}")

    def load_config(self):
        try:
            config_dir = 'config/DoEx'  # 設定config目錄，會自動讀取全部檔案
            self.config_data = ConfigLoader(config_dir).config_dict
            logging.info('DoEx: Config loaded')
        except Exception as e:
            logging.error(f"DoEx: Error loading experiment config-{e}")

    def create_path(self):
        try:
            self.data_saver = DataSaver(self.config_data)  # 初始化 儲存器物件
            self.config_data['path']['output_dir-final'] = self.data_saver.dir_path  # 設定資料夾
            logging.info('DoEx: path created')
        except Exception as e:
            logging.error(f"DoEx: Error creating path-{e}")

    def start_audio_experiment(self):
        try:
            logging.info('DoEx: Starting_Ex')
            self.Send_State.send_status("Starting_Ex")
            self.Audio_Experiment = AudioExperiment(self.config_data)  # 初始化 實驗物件
            self.Audio_Experiment.run_experiment()  # 執行實驗
        except Exception as e:
            logging.error(f"DoEx: Error starting audio experiment-{e}")

    def wait_for_completion(self):
        try:
            while self.Audio_Experiment.get_is_handle_finish() is False:  # 等待實驗完成
                time.sleep(0.1)  # 暫停1秒
        except Exception as e:
            logging.error(f"DoEx:Error during audio experiment-{e}")

    def save_results(self):
        try:
            self.data_saver.save_data_to_json(
                self.Audio_Experiment.get_handle_results(),
                self.config_data['path']['output_data_filename'])  # 儲存實驗結果
            self.Send_State.send_status("Finish_Ex")
            logging.info('DoEx: Finish_Ex')
        except Exception as e:
            logging.error(f"Error saving experiment results:-{e}")

    def upload_files(self):
        try:
            uploader = FileUploader(self.System_config_data, self.data_saver.dir_path)  # 建立一個FileUploader實例
            uploader.upload_files()  # 上傳所有檔案
            self.Send_State.send_status("finish_upload_files")
            logging.info('DoEx: finish_upload_files')
        except Exception as e:
            logging.error(f"Error uploading files: {e}")

    def run(self):
        self.start_experiment()
        self.load_config()
        self.create_path()
        self.start_audio_experiment()
        self.wait_for_completion()
        self.save_results()
        self.upload_files()

if __name__ == "__main__":
    experiment = Experiment()  # 創建一個 Experiment 實例
    experiment.run()  # 運行實驗

import os
import requests
import json
import time
from datetime import datetime

# 向伺服器傳輸狀態的類別
class BasicServerConnect:

    def __init__(self,Config): # 初始化
        self.server_ip = Config['Server']['server_ip']      # 伺服器IP
        self.server_port = Config['Server']['server_port']  # 伺服器port
        self.device_type = Config['Server']['device_type']  # 設備類別
        self.client_id = Config['Server']['edgeid']         # 設備編號
        
        self.server_url = self._build_server_url()          # 建立伺服器連結
        self.status_ip = self._build_status_ip()            # 建立狀態傳輸網址
        
        # 檢查伺服器連接
        self.server_connected = self._check_server_connection()

    def _build_server_url(self): # 建立伺服器連結的方法
        return f"http://{self.server_ip}:{self.server_port}"

    def _build_status_ip(self): # 建立狀態傳輸網址的方法
        return f"{self.server_url}/status"

    def _check_server_connection(self): # 檢查伺服器連接的方法
        try:
            response = requests.get( f"{self.server_url}/connect_test")
            return response.status_code == 200
        except:
            return False

    def send_status(self, status): # 所有傳輸狀態的資料的方法
        if not self.server_connected:
            print("無法連接到伺服器。")
            return

        headers = {'Content-Type': 'application/json'}
        data = {'status': status,
                'device_id': self.client_id,
                'device_type': self.device_type,
                'timestamp': datetime.now().isoformat()}
        
        response = requests.post(self.status_ip, headers=headers, data=json.dumps(data))
        print(response.json())

# 向伺服器傳輸檔案的類別，繼承自 BasicServerConnect 類別
class FileUploader(BasicServerConnect):

    def __init__(self, Config, folder): # 初始化
        super().__init__(Config)
        self.session_id = folder.replace('out/', '')       # session id，從 folder 名稱中取得
        self.directory = folder                            # 要上傳的檔案所在目錄
        self.MAX_RETRIES = Config['Server']['max_retry']   # 最高重試次數
        self.RETRY_DELAY = Config['Server']['retry_delay'] # 每次重試等待間隔

        self.files_upload_ip = self._build_files_upload_ip() # 建立上傳檔案的連結

    def _build_files_upload_ip(self): # 建立上傳檔案的連結的方法
        return f"{self.server_url}/input/{self.client_id}/{self.session_id}/"

    def upload_file(self, filename): # 調度檔案上傳的方法
        file_path = os.path.join(self.directory, filename)
        with open(file_path, 'rb') as file:
            self._attempt_upload(file, filename)

    def _attempt_upload(self, file, filename): # 單檔案上傳管理器的方法
        for i in range(self.MAX_RETRIES):
            if self._upload(file, filename):
                break
            if i < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_DELAY)
                print(f"重新上傳 {filename}! {i}/{self.MAX_RETRIES}")

    def _upload(self, file, filename): # 單檔案上傳的方法
        try:
            response = requests.post(self.files_upload_ip, files={'file': file})
            if response.status_code == 200:
                print(f"成功上傳 {filename}!")
                return True
            else:
                print(f"上傳 {filename} 失敗. 錯誤碼: {response.status_code}")
        except Exception as e:
            print(f"上傳 {filename} 時發生錯誤: {str(e)}")
        return False

    def upload_files(self): # 上傳目錄中所有檔案的方法
        filenames = os.listdir(self.directory)
        
        for f in filenames:
            self.upload_file(f)

# 範例 main 程式
if __name__ == "__main__":
    #### 執行前必備 ####
    os.chdir("/home/led/project/Basic-experimental-framework")  
    from ConfigLoader import ConfigLoader
    System_config_dir = 'config' # 設定config目錄，會自動讀取全部檔案
    System_config_data = ConfigLoader(System_config_dir).config_dict
    ###################
    
    #範例1 上傳out/out-test中的所有檔案
    uploader = FileUploader(System_config_data, "out/out-test")  # 建立一個FileUploader實例
    uploader.upload_files()  # 上傳 out/out-test/ 中的所有檔案
    uploader.send_status("finish-upload-files")  # 傳送 "finish-upload-files" 狀態到伺服器

    time.sleep(5) #等待一下，讓你有時間確認結果

    #範例2 傳送 "hihi" 狀態到伺服器
    ServerState = BasicServerConnect(System_config_data)  # 建立一個BasicServerConnect實例
    ServerState.send_status("hihi")  # 傳送 "hihi" 狀態到伺服器

    # happy coding (*′∀`)~♥
    # By LED

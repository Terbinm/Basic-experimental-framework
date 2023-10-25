import os
import requests
from concurrent.futures import ThreadPoolExecutor
import json
import time
from datetime import datetime

class BasicServerConnect:
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # delay in seconds

    def __init__(self, client_id, folder):
        self.client_id = client_id
        self.folder = folder
        self.server_url = self._build_server_url()
        self.files_upload_ip = self._build_files_upload_ip()
        self.status_ip = self._build_status_ip()
        self.directory = folder

    def _build_server_url(self):
        server_ip = "127.0.0.1"
        server_port = "9999"
        return f"http://{server_ip}:{server_port}"

    def _build_files_upload_ip(self):
        return f"{self.server_url}/input/{self.client_id}/{self.folder}/"

    def _build_status_ip(self):
        return f"{self.server_url}/status"

    def send_status(self, status):
        headers = {'Content-Type': 'application/json'}
        data = {'device_id': self.client_id, 'status': status, 'timestamp': datetime.now().isoformat()}
        response = requests.post(self.status_ip, headers=headers, data=json.dumps(data))
        print(response.json())

    def upload_file(self, filename):
        file_path = os.path.join(self.directory, filename)
        with open(file_path, 'rb') as file:
            self._attempt_upload(file, filename)

    def _attempt_upload(self, file, filename):
        for i in range(self.MAX_RETRIES):
            if self._upload(file, filename):
                break
            if i < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_DELAY)
                print(f"Retry {filename}!")

    def _upload(self, file, filename):
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

    def upload_files(self):
        filenames = os.listdir(self.directory)

        #單執行緒
        for f in filenames:
            self.upload_file(f)
            
        #多執行緒
        # with ThreadPoolExecutor() as executor:
        #     executor.map(self.upload_file, filenames)

# uploader = BasicServerConnect("233", "B")  # 建立一個FileUploader實例
# uploader.upload_files()  # 上傳 out/A/ 中的所有檔案

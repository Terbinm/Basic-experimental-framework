import os
import json
from datetime import datetime

class DataSaver:
    def __init__(self,config_data):
        self.dir_path = None
        self.out_base_path = config_data['path']['output_dir']

        self.create_directory(config_data)

    def create_directory(self,config_data):
        # 建立一個名為當前時間戳的資料夾於out資料夾下

        # 支持自定義命名
        # path_set = None
        # if not config_data['path']['output_dir-final']:
        #     now = datetime.now()
        #     path_set = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
        #     config_data['path']['output_dir-final'] = path_set
        # else:
        #     path_set = config_data['path']['output_dir-final']


        # 不支持自定義命名
        path_set = None
        now = datetime.now()
        path_set = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
        config_data['path']['output_dir-final'] = path_set

        self.dir_path = os.path.join(self.out_base_path, path_set)
        os.makedirs(self.dir_path, exist_ok=True)

        print(f"自動建立資料夾 - {self.dir_path}")
        self.save_data_to_json(config_data,"config")


    def save_data_to_json(self,config,name):
        # 將當前目錄與config字典打包為json檔後保存於資料夾中
        with open(os.path.join(self.dir_path, name+'.json'), 'w') as f:
            json.dump(config, f, indent=4)

    def get_dir_path(self):
        return self.dir_path

import os
import json
from datetime import datetime

class DataSaver:
    def __init__(self,config_data):
        self.dir_path = None
        self.out_base_path = config_data['path']['output_dir']

        self.create_outdir = self.create_timestamp_directory()

    def create_timestamp_directory(self):
        # 建立一個名為當前時間戳的資料夾於out資料夾下
        now = datetime.now()
        timestamp = str(now.strftime("%Y-%m-%d %H-%M-%S"))
        self.dir_path = os.path.join(self.out_base_path, timestamp)
        os.makedirs(self.dir_path, exist_ok=True)

    def save_data_to_json(self,config,name):
        # 將當前目錄與config字典打包為json檔後保存於資料夾中
        # data = {
        #     "current_directory": os.getcwd(),
        #     "config": config,
        # }
        with open(os.path.join(self.dir_path, name+'.json'), 'w') as f:
            json.dump(config, f, indent=4)

    def save(self,config,name):
        self.create_outdir
        self.save_data_to_json(config,name)


    def get_dir_path(self):
        return self.dir_path

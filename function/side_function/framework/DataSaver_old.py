import os
import json
from datetime import datetime

class DataSaver:
    def __init__(self, config):
        self.config = config
        self.dir_path = None

    def save(self):
        # 建立一個名為當前時間戳的資料夾於out資料夾下
        now = datetime.now()
        timestamp = str(now.strftime("%Y-%m-%d %H-%M-%S"))
        self.dir_path = os.path.join('out', timestamp)
        os.makedirs(self.dir_path, exist_ok=True)

        # 將當前目錄與config字典打包為json檔後保存於資料夾中
        data = {
            "current_directory": os.getcwd(),
            "config": self.config,
        }
        with open(os.path.join(self.dir_path, 'data.json'), 'w') as f:
            json.dump(data, f, indent=4)

    def get_dir_path(self):
        return self.dir_path

# 測試用的Python程式碼 全部寫在一起，重構
if __name__ == "__main__":
    # 假設這是您的config字典
    config = {
        "key1": "value1",
        "key2": "value2",
        # ...
    }

    data_saver = DataSaver(config)
    data_saver.save()
    print(data_saver.get_dir_path())

import configparser

class ConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config_dict = self.load_config()

    def load_config(self):
        # 創建配置解析器對象
        config = configparser.ConfigParser()

        # 讀取指定的配置文件
        config.read(self.file_path)

        # 將配置數據讀取到一個字典中
        config_dict = {s:dict(config.items(s)) for s in config.sections()}

        return config_dict

# 只讀一個檔案，沒有任何後處理
# 使用示例
# config_loader = ConfigLoader('test.ini')
# print(config_loader.config_dict)

import configparser
import os
import concurrent.futures

class ConfigLoader:
    def __init__(self, config_dir):
        self.config_dir = config_dir

        self.config_dict = self.load_all_configs()

    def convert_value(self, value):
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        return value

    def load_config(self, file_path):
        config = configparser.ConfigParser()
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        cleaned_lines = [line.split('#')[0] + '\n' for line in lines]
        config.read_string(''.join(cleaned_lines))
        config_dict = {s: {k: self.convert_value(v) for k, v in config.items(s)} for s in config.sections()}
        return config_dict

    def load_all_configs(self):
        ini_files = [os.path.join(self.config_dir, f) for f in os.listdir(self.config_dir) if f.endswith('.ini')]
        all_configs = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self.load_config, file): file for file in ini_files}
            for future in concurrent.futures.as_completed(future_to_file):
                try:
                    data = future.result()
                except Exception as exc:
                    print(f'Generated an exception: {exc}')
                else:
                    all_configs.update(data)

        return all_configs

# 測試用
# config_loader = ConfigLoader('config')
# print(config_loader.config_dict)

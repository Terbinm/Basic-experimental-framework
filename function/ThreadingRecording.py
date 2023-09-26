import threading
import time

class AudioExperiment:
    def __init__(self, config_data):
        self.config_data = config_data

        #時間戳紀錄
        self.play_time_result = None
        self.record_time_result = None

        #是否執行完畢-flag
        self.is_play_finish = False
        self.is_record_finish = False
        self.is_handle_finish = False

        self.handle_results = None



    def play_audio(self, filename):
        # 開始時間
        start_time = time.time()

        # 播放音樂
        time.sleep(3)
        # 結束時間
        end_time = time.time()


        self.play_time_result = start_time, end_time #設定本次時間點
        self.is_play_finish = True #立flag


    def record_audio(self, filename, duration):
        # 開始時間
        start_time = time.time()

        # 錄音
        time.sleep(3)

        # 結束時間
        end_time = time.time()

        self.record_time_result = start_time, end_time #設定本次時間點
        self.is_record_finish = True #立flag

    def process_results(self):
        # 確保兩個執行緒都已經完成
        while self.is_record_finish is False or self.is_play_finish is False:
            time.sleep(0.1)  # 等待結果

        # 取得結果
        play_start, play_end = self.play_time_result
        record_start, record_end = self.record_time_result

        # 處理結果（這裡只是將結果印出，你可以根據你的需求來修改）
        print(f"播放音樂的時間差: {play_end - play_start}")
        print(f"錄音的時間差: {record_end - record_start}")

        # 建立一個字典來儲存你的變數
        results = {
            'play_result': self.play_time_result,
            'record_result': self.record_time_result,
            'is_play_finish': self.is_play_finish,
            'is_record_finish': self.is_record_finish
        }
        self.handle_results = results
        self.is_handle_finish = True #立flag


    def run_experiment(self):
        play_filename = self.config_data['Experiment']['play_filename']
        record_filename = self.config_data['Experiment']['record_filename']
        record_duration = self.config_data['Experiment']['record_duration']
        # ... (將config參數儲存並傳入)

        play_thread = threading.Thread(target=self.play_audio, args=(play_filename,))
        record_thread = threading.Thread(target=self.record_audio, args=(record_filename, record_duration))

        play_thread.start()
        record_thread.start()

        play_thread.join()
        record_thread.join()


        self.process_results()
        # 使用時一定要以物件使用，不可重複使用物件(宣告一個新的或繼承)

    def get_handle_results(self):
        return self.handle_results

    def get_is_handle_finish(self):
        return self.is_handle_finish

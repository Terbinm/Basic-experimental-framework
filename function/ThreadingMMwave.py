import threading
import time
import os
import sys


class MMwaveExperiment:
    def __init__(self, config_data):
        self.config_data = config_data
        # print(config_data)
        #時間戳紀錄
        self.experiment_time_result = None
        self.play_time_result = None
        self.record_time_result = None

        #是否執行完畢-flag
        self.is_play_finish = False
        self.is_record_finish = False
        self.is_handle_finish = False

        self.handle_results = None
        self.set_time_out = config_data['set']['handle_time_out']  # 取樣頻率
        self.status = {
            'Experiment': "MMwave"
                       } #狀態輸出資訊

        #Audio配置檔讀取
        self.sampling_rate = config_data['Audio']['sampling_rate']  # 取樣頻率
        self.record_duration = config_data['Audio']['record_duration']  # 錄音時間，單位為秒
        self.record_filename = config_data['Audio']['record_filename']  # 錄音檔名
        self.play_filename = config_data['Audio']['play_filename']   # 播放音樂
        self.final_dir = config_data['path']['output_dir-final']  # 最終目錄
        self.input_dir = config_data['path']['input_dir']  # 輸入目錄


    def play_audio(self):
        pass
        # # 開始時間
        # start_time = time.time()
        # print(os.path.join(self.input_dir, self.play_filename))
        # # pygame.mixer.init()
        
        # # pygame.mixer.music.load(os.path.join(self.input_dir, self.play_filename))

        # # pygame.mixer.init()
        # # # 播放音樂
        # # pygame.mixer.music.play()

        # # # 等待音檔播放完畢
        # # while pygame.mixer.music.get_busy() == True:
        # #     continue

        # soundfile= os.path.join(self.input_dir, self.play_filename)
        # song=AudioSegment.from_wav(soundfile)
        # play(song)

        # # 結束時間
        # end_time = time.time()

        # self.play_time_result = start_time, end_time #設定本次時間點
        # self.is_play_finish = True #立flag

    def record_audio(self):
        pass
        # 開始時間
        # start_time = time.time()

        # # 錄音
        # recording = sd.rec(int(self.record_duration * self.sampling_rate), samplerate=self.sampling_rate, channels=1)
        # sd.wait()  # 等待錄音結束

        # # 結束時間
        # end_time = time.time()

        # # 建立完整的檔案路徑並寫入錄音檔案
        # full_path = os.path.join(self.final_dir, self.record_filename)
        # write(full_path, self.sampling_rate, recording)

        # self.record_time_result = start_time, end_time #設定本次時間點
        # self.is_record_finish = True #立flag
    
    def run_experiment(self):
        play_thread = threading.Thread(target=self.play_audio, args=())
        record_thread = threading.Thread(target=self.record_audio, args=())

        self.experiment_time_result = time.time()
        # play_thread.start()
        record_thread.start()

        # play_thread.join()
        record_thread.join()


        self.process_results_debug()
        # 使用時一定要以物件使用，不可重複使用物件(宣告一個新的或繼承)


    def process_results(self):
        # 確保兩個執行緒都已經完成
        while self.is_record_finish is False or self.is_play_finish is False:
            time.sleep(0.5)  # 等待結果
            print("wait for processing")

        # 取得結果
        play_start, play_end = self.play_time_result
        record_start, record_end = self.record_time_result

        # 處理結果（這裡只是將結果印出，你可以根據你的需求來修改）
        print(f"播放音樂的時間差: {play_end - play_start}")
        print(f"錄音的時間差: {record_end - record_start}")

        # 建立一個字典來儲存你的變數
        results = {
            'experiment_time_result': self.experiment_time_result,
            'play_result': self.play_time_result,
            'record_result': self.record_time_result,
            'is_play_finish': self.is_play_finish,
            'is_record_finish': self.is_record_finish
        }
        self.handle_results = results
        self.is_handle_finish = True #立flag


    
    def wait_for_processing(self):
        time_out = 0
        status = 200
        while self.is_record_finish is False or self.is_play_finish is False:
            time_out +=1
            print(f"wait for processing --- {time_out} / {self.set_time_out}")
            if time_out >= self.set_time_out:
                print("Timeout")
                status = 408 
                break
            time.sleep(1)  # 等待結果
        
        return status
    
    def handle_play_time_result(self):
        try:
            play_start, play_end = self.play_time_result
            print(f"播放音樂的時間差: {play_end - play_start}")
        except:
            print(f"play sound fail")
   
    def handle_record_time_result(self):
        try:
            record_start, record_end = self.record_time_result
            print(f"錄音的時間差: {record_end - record_start}")
        except:
            print(f"record sound fail")

    def process_results_debug(self):
        # 確保兩個執行緒都已經完成
        time_out = 0

        self.status['process_handle_results'] = self.wait_for_processing()

        # 取得結果
        self.handle_play_time_result()
        self.handle_record_time_result()

        # 建立一個字典來儲存你的變數
        results = {
            'experiment_time_result': self.experiment_time_result,
            'play_result': self.play_time_result,
            'record_result': self.record_time_result,
            'is_play_finish': self.is_play_finish,
            'is_record_finish': self.is_record_finish,


            'process_status': self.status
        }
        self.handle_results = results
        self.is_handle_finish = True #立flag


    def get_handle_results(self):
        return self.handle_results

    def get_is_handle_finish(self):
        return self.is_handle_finish

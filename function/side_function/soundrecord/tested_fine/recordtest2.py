import sounddevice as sd
from scipy.io.wavfile import write

# 錄音參數
fs = 44100  # 取樣頻率
duration = 5  # 錄音時間，單位為秒

# 錄音
print("開始錄音...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()  # 等待錄音結束
print("錄音結束")

# 儲存錄音檔案
write('output.wav', fs, recording)

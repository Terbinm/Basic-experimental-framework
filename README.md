# Basic-experimental-framework
讀取config，並進行實驗後記錄 (以聲音錄製+撥放為例)

    # 設置GPIO模式為BCM
    GPIO.setmode(GPIO.BCM)

    # 定義按鈕和LED的GPIO針腳
    button_pins = [17, 27, 22]  # 三個按鈕的GPIO針腳
    led_pins = [2, 3, 4]  # 三個LED的GPIO針腳 #紅，橘，綠

***尚未寫說明***
## config
A組配置檔，含部分B、C三組
## data
音檔存放處
## function
old_function:已淘汰的測試function
錄音、撥放、處理config參數、自動建立時間資料夾、output應記事項
## out
輸出的時間戳記資料夾、wav檔、json檔
## Test_function
測試程式暫存場所
## venv
source /home/led/project/Basic-experimental-framework/venv/project_venv/bin/activate
## client.py
run的時候要用這個
cd /home/led/project/Basic-experimental-framework/
## output.wav
## server.py
## test.py
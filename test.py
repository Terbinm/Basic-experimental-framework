import logging

# 設定日誌紀錄的等級並將日誌訊息寫入到檔案中
logging.basicConfig(filename='example.log', level=logging.DEBUG)

# 根據不同的情況記錄日誌
logging.debug('這是 debug 等級的訊息')
logging.info('這是 info 等級的訊息')
logging.warning('這是 warning 等級的訊息')
logging.error('這是 error 等級的訊息')
logging.critical('這是 critical 等級的訊息')
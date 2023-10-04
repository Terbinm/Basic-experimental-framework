import pygame

# 初始化 mixer
pygame.mixer.init()

# 載入你的音檔
pygame.mixer.music.load("data/play.mp3")

# 播放音檔
pygame.mixer.music.play()

# 等待音檔播放完畢
while pygame.mixer.music.get_busy() == True:
    continue

# import time
#
# from playsound import playsound
# from utility.logger import Logger as log
#
# while True:
#     file_path = "data/hands/warn.mp3"
#     playsound(file_path, True)
#     log.logdebug("Done")
#     time.sleep(4)


import pygame

pygame.init()

mp3_file = "data/hands/warn.mp3"

pygame.mixer.init()
pygame.mixer.music.load(mp3_file)

pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

pygame.mixer.quit()
pygame.quit()

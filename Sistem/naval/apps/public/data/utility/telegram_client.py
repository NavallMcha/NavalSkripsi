import cv2
import telebot


# pip install pyTelegramBotAPI
class TelegramClient:
    def __init__(self, token):
        self.token = token
        self.bot = self._create_bot()

    def _create_bot(self):
        bot = telebot.TeleBot(self.token)
        return bot

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id, text)

    def send_imagecv2(self, chat_id, image):
        # convert frame OpenCV to data JPEG
        _, jpeg_image = cv2.imencode(".jpg", image)
        # send image
        self.bot.send_photo(chat_id, photo=jpeg_image.tobytes())

    def start_polling(self):
        self.bot.polling(none_stop=True, interval=0, timeout=20)

    def stop_polling(self):
        self.bot.stop_polling()

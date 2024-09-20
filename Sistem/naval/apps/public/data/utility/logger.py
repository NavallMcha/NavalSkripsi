import time
from colorama import init, Fore, Style, Back


class Logger:
    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def logdebug(msg):
        print(Style.BRIGHT + Fore.GREEN + f"[DEBUG] [{time.time()}]: " + str(
            msg) + Fore.RESET + Back.RESET + Style.RESET_ALL)

    @staticmethod
    def loginfo(msg):
        print(Style.BRIGHT + Fore.RESET + f"[INFO] [{time.time()}]: " + str(
            msg) + Fore.RESET + Back.RESET + Style.RESET_ALL)

    @staticmethod
    def logwarn(msg):
        print(Style.BRIGHT + Fore.YELLOW + f"[WARNING] [{time.time()}]: " + str(
            msg) + Fore.RESET + Back.RESET + Style.RESET_ALL)

    @staticmethod
    def logerr(msg):
        print(
            Style.BRIGHT + Fore.RED + f"[ERROR] [{time.time()}]: " + str(
                msg) + Fore.RESET + Back.RESET + Style.RESET_ALL)

    @staticmethod
    def logsilent(msg):
        pass

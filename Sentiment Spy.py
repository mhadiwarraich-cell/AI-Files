import colorama
from colorama import Fore, Style
from textblob  import Textblob


colorama.init()


print(f"{Fore.CYAN} Welcome to Sentiment Spy! {Style.RESET_ALL}")


user_name = input(f"{Fore.MAGENTA}Please enter your name: {Style.RESET_ALL}")


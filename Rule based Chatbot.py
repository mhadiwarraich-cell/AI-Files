import re, random
from colorama import Fore, init
init(autoreset=True)


destination = {
    "beaches": ["Bali", "Maldives", "Phuket"],
    "mountains": ["Swiss Alps", "Rockey Mountains", "Himalayas"],
    "cities":["Tokyo", "Parid", "New York"]
}

jokes = [
    "Why don't programmers like nature? Too many bugs!"
    "Why did the computer go to the doctor? Because it had a virus!"
    "Why do travelers always feeel warm? Because of all their hot spots!"


    def normalize_input(text):
        return re.sub(r"\s+", "", text.strip().lower())

    def recommend():
        print(Fore,CYAN + "TravelBot: Beaches, mountains, or cities?")
        preference = input(Fore.YELLOW + "You: ")
        preference = normalize_input(preference)






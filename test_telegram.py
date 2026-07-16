import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def envoyer_message(texte):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texte
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("Message envoyé avec succès !")
    else:
        print(f"Erreur {response.status_code} : {response.text}")

if __name__ == "__main__":
    envoyer_message("Test : mon bot fonctionne 🎉")
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()  # charge les variables du fichier .env

TOKEN = os.getenv("LBA_API_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FICHIER_SUIVI = "offres_envoyees.json"




def charger_offres_envoyees():
    """Charge la liste des IDs déjà envoyés, ou une liste vide si le fichier n'existe pas encore"""
    if os.path.exists(FICHIER_SUIVI):
        with open(FICHIER_SUIVI, "r") as f:
            return set(json.load(f))
    return set()


def sauvegarder_offres_envoyees(ids_envoyes):
    """Sauvegarde la liste des IDs envoyés dans le fichier"""
    with open(FICHIER_SUIVI, "w") as f:
        json.dump(list(ids_envoyes), f)


def rechercher_offres():
    url = "https://api.apprentissage.beta.gouv.fr/api/job/v1/search"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    params = {
        "romes": "M1805",           # code ROME "Études et développement informatique"
        "longitude": 2.3522,          # Paris
        "latitude": 48.8566,
        "radius": 30,                 # rayon en km
        "target_diploma_level": "5"   # niveau bac (à ajuster selon tes critères)
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None

def filtrer_offres(jobs, mots_cles):
    """Ne garde que les offres dont le titre ou la description contient un des mots-clés"""
    offres_filtrees = []
    
    for job in jobs:
        titre = job["offer"]["title"].lower()
        description = job["offer"]["description"].lower()
        
        for mot in mots_cles:
            if mot.lower() in titre or mot.lower() in description:
                offres_filtrees.append(job)
                break  # pas besoin de vérifier les autres mots-clés une fois qu'on a matché
    
    return offres_filtrees

def dedupliquer_offres(jobs):
    """Supprime les offres en double (même titre + même adresse)"""
    offres_vues = set()
    offres_uniques = []
    
    for job in jobs:
        titre = job["offer"]["title"]
        adresse = job["workplace"]["location"]["address"]
        cle = (titre, adresse)  # un tuple unique pour identifier l'offre
        
        if cle not in offres_vues:
            offres_vues.add(cle)
            offres_uniques.append(job)
    
    return offres_uniques

def envoyer_message(texte):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texte
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Erreur envoi Telegram : {response.text}")

def formater_offre(job):
    """Transforme une offre en message texte lisible pour Telegram"""
    titre = job["offer"]["title"]
    adresse = job["workplace"]["location"]["address"]
    lien = job["apply"]["url"]
    
    return f"📌 {titre}\n📍 {adresse}\n🔗 {lien}"


if __name__ == "__main__":
    resultats = rechercher_offres()
    
    if resultats:
        jobs = resultats["jobs"]
        
        mots_cles = ["web", "développeur", "développement"]
        offres_pertinentes = filtrer_offres(jobs, mots_cles)
        offres_uniques = dedupliquer_offres(offres_pertinentes)
        
        # On charge les offres déjà envoyées lors des exécutions précédentes
        ids_deja_envoyes = charger_offres_envoyees()
        
        # On ne garde que les offres jamais envoyées
        nouvelles_offres = [
            job for job in offres_uniques 
            if job["identifier"]["id"] not in ids_deja_envoyes
        ]
        
        print(f"{len(nouvelles_offres)} nouvelle(s) offre(s) à envoyer")
        
        if nouvelles_offres:
            for job in nouvelles_offres:
                message = formater_offre(job)
                envoyer_message(message)
                ids_deja_envoyes.add(job["identifier"]["id"])
                print("Offre envoyée :", job["offer"]["title"])
            
            # On sauvegarde la liste mise à jour
            sauvegarder_offres_envoyees(ids_deja_envoyes)
        else:
            print("Aucune nouvelle offre à envoyer")
            envoyer_message("Aucune nouvelle offre à envoyer :/")
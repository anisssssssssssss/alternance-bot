Bot automatisé qui surveille les nouvelles offres d'alternance en informatique 
(Île-de-France) et envoie une alerte Telegram en temps réel dès qu'une offre 
correspondant à mes critères est publiée.

## Pourquoi ce projet

En pleine recherche d'alternance, je perdais du temps à vérifier manuellement 
plusieurs sites plusieurs fois par jour. Ce bot automatise la veille et me 
notifie directement sur Telegram, sans action de ma part.

## Stack technique

- **Python** — logique métier (récupération, filtrage, déduplication)
- **API La Bonne Alternance** (api.apprentissage.beta.gouv.fr) — source des offres
- **API Telegram Bot** — envoi des notifications
- **GitHub Actions** — exécution automatisée toutes les 3h, sans serveur à gérer
- **JSON** — persistance légère pour éviter les doublons entre exécutions

## Fonctionnement

1. Le script interroge l'API La Bonne Alternance selon des critères définis 
   (métier, localisation, niveau de diplôme)
2. Filtre les résultats sur des mots-clés pertinents (titre/description)
3. Déduplique les offres (l'API agrège plusieurs sources pouvant renvoyer 
   la même offre)
4. Compare avec les offres déjà envoyées (fichier de suivi)
5. Envoie uniquement les nouvelles offres via Telegram
6. GitHub Actions répète ce processus automatiquement toutes les 3h

## Installation

bash :

git clone https://github.com/TON_USERNAME/alternance-bot.git
cd alternance-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Crée un fichier `.env` à la racine avec :

LBA_API_TOKEN=ton_token
TELEGRAM_TOKEN=ton_token
TELEGRAM_CHAT_ID=ton_chat_id

Et executer :
python3 main.py




## Améliorations possibles

- Interface web pour configurer les critères sans toucher au code
- Support de plusieurs sources (scraping Indeed/LinkedIn en complément de l'API)
- Base de données SQLite plutôt qu'un fichier JSON pour le suivi

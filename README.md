# Alternance Bot

Bot automatisé qui surveille les nouvelles offres d'alternance en informatique
(Île-de-France) et envoie une alerte Telegram en temps réel dès qu'une offre
correspondant à mes critères est publiée. Les critères de recherche sont
configurables via une interface web, sans toucher au code.

## Pourquoi ce projet

En pleine recherche d'alternance, je perdais du temps à vérifier manuellement
plusieurs sites plusieurs fois par jour. Ce bot automatise la veille et me
notifie directement sur Telegram, sans action de ma part.

## Stack technique

- **Python** — logique métier (récupération, filtrage, déduplication)
- **API La Bonne Alternance** (api.apprentissage.beta.gouv.fr) — source des offres
- **API Telegram Bot** — envoi des notifications
- **Flask** — backend de l'interface de configuration
- **PostgreSQL** (hébergé sur Render) — stockage des critères de recherche
- **Render** — hébergement du backend web, accessible en continu
- **GitHub Actions** — exécution automatisée du bot toutes les 3h, sans serveur à gérer
- **JSON** — persistance légère pour éviter les doublons entre exécutions

## Architecture

Interface web (Render) en lien avec la base PostgreSQL (Render).

`main.py`, exécuté par GitHub Actions toutes les 3h, appelle `GET /criteres`
sur cette interface pour récupérer les critères de recherche, puis interroge
l'API La Bonne Alternance, filtre, déduplique, et envoie les nouvelles offres
sur Telegram.

## Fonctionnement

1. Les critères de recherche (mots-clés, métier, localisation, rayon, niveau
   de diplôme) sont configurés via une interface web et stockés en base
   PostgreSQL
2. Toutes les 3h, GitHub Actions exécute `main.py`, qui récupère ces critères
   via l'API du backend Flask
3. Le script interroge l'API La Bonne Alternance selon ces critères
4. Filtre les résultats sur les mots-clés pertinents (titre/description)
5. Déduplique les offres (l'API agrège plusieurs sources pouvant renvoyer
   la même offre)
6. Compare avec les offres déjà envoyées (fichier de suivi)
7. Envoie uniquement les nouvelles offres via Telegram

## Installation

### Bot (main.py)

Clone le repo, crée un environnement virtuel, active-le, puis installe les
dépendances avec `pip install -r requirements.txt`.

Crée un fichier `.env` à la racine avec :

```
LBA_API_TOKEN=ton_token
TELEGRAM_TOKEN=ton_token
TELEGRAM_CHAT_ID=ton_chat_id
```

Lance ensuite le bot avec `python3 main.py`.

### Interface web (app.py)

Lance `python3 app.py`, puis va sur `http://127.0.0.1:5000` pour configurer
les critères en local (base SQLite par défaut). En production, l'interface
tourne sur Render et utilise PostgreSQL via la variable d'environnement
`DATABASE_URL`.


## Améliorations possibles

- Support de plusieurs sources (scraping Indeed/LinkedIn en complément de l'API)

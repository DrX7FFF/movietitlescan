import requests
import json

def search_jackett(movie_name, jackett_api_url, jackett_api_key, indexer="all", category="2000"):
    params = {
        "apikey": jackett_api_key,
        "t": "search",
        "cat": category,
        "q": movie_name,
        "tracker": indexer
    }
    response = requests.get(jackett_api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

# Exemple d'utilisation
JACKETT_API_URL = "http://localhost:9117/api/v2.0/indexers/all/results"
JACKETT_API_KEY = "VOTRE_CLE_API"
MOVIE_NAME = "Braquage à l'ancienne"

results = search_jackett(MOVIE_NAME, JACKETT_API_URL, JACKETT_API_KEY)
if results:
    with open("jackett_results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
    print("Résultats enregistrés dans jackett_results.json")

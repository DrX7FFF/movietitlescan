import re
import json

# Charger le dictionnaire depuis un fichier JSON
DEFAULT_DICTIONARY = {
    "tags": {
        "MKV": ["format"],
        "MP4": ["format"],
        "AVI": ["format"],
        "BluRay": ["source"],
        "BR": ["source"],
        "DVD": ["source", "480p"],
        "1080p": ["resolution"],
        "720p": ["resolution"],
        "x264": ["codec"],
        "x265": ["codec"],
        "H264": ["codec"],
        "H265": ["codec"],
        "HEVC": ["codec"],
        "VOSTFR": ["language"],
        "FRENCH": ["language"],
        "TRUEFRENCH": ["language"]
    },
    "synonyms": {
        "BR": "BluRay",
        "x264": "H264",
        "x265": "H265",
        "HEVC": "H265",
        "TRUEFRENCH": "FRENCH"
    }
}

def load_dictionary(filename="tags.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return DEFAULT_DICTIONARY.copy()

def save_dictionary(dictionary, filename="tags.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)

# Charger les tags et synonymes
dictionary = load_dictionary()
tag_dict = dictionary.get("tags", {})
synonyms = dictionary.get("synonyms", {})

def extract_title_and_year(filename, movie_title, movie_year):
    pattern = re.escape(movie_title) + r".*?\b(" + re.escape(str(movie_year)) + r")\b"
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        cleaned_filename = re.sub(pattern, "", filename, flags=re.IGNORECASE).strip()
        return cleaned_filename
    return None

def parse_filename(filename, movie_title, movie_year):
    cleaned_filename = extract_title_and_year(filename, movie_title, movie_year)
    if not cleaned_filename:
        return None, []  # Le fichier ne correspond pas au film recherché
    
    words = re.split(r'\W+', cleaned_filename)  # Découpe sur tout ce qui n'est pas alphanumérique
    detected_tags = {}
    unknown_words = []
    
    for word in words:
        word = synonyms.get(word, word)  # Remplace par le synonyme si existant
        if word in tag_dict:
            for category in tag_dict[word]:
                detected_tags[category] = word
        else:
            unknown_words.append(word)
    
    # Ajouter les mots inconnus au dictionnaire
    for word in unknown_words:
        if word not in tag_dict:
            tag_dict[word] = []
    
    return detected_tags, unknown_words

# Film recherché
movie_title = "Braquage à l'ancienne"
movie_year = 2017

# Test avec les fichiers donnés
files = [
    "Braquage à l'ancienne 2017 VOSTFR BluRay 720p FREELEECH",
    "Braquage à l'ancienne 2017 FRENCH BluRay 720p FREELEECH",
    "Braquage à l'ancienne 2017 TRUEFRENCH DVDRIP FREELEECH",
]

for file in files:
    tags, unknowns = parse_filename(file, movie_title, movie_year)
    if tags is not None:
        print(f"{file}: {tags}")
        if unknowns:
            print(f"  Mots inconnus: {unknowns}")
    else:
        print(f"{file}: Ne correspond pas au film recherché")

# Sauvegarde du dictionnaire mis à jour
save_dictionary({"tags": tag_dict, "synonyms": synonyms})

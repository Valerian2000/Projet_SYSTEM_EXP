import psycopg2
from rapidfuzz.distance import Levenshtein
import unicodedata

# ----------------------------
# 1. Connexion PostgreSQL
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="DB001",
    user="postgres",
    password="14062000"
)



try:
    with conn.cursor() as cur:
        # Création de la table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phrases (
                id SERIAL PRIMARY KEY,
                texte TEXT
            );
        """)

        # Insertion des données
        cur.execute("""
            INSERT INTO phrases (texte) VALUES
            ('le chat noir'),
            ('le chat blanc'),
            ('un chien court'),
            ('je mange une pomme'),
            ('je mange une grosse pomme'),
            ('la voiture roule vite');
        """)

    # Sauvegarde
    conn.commit()
    print(" Table 'phrases' créée et données insérées.")

except Exception as e:
    print(" Erreur :", e)
    conn.rollback()

# ----------------------------
# 2. Normalisation français
# ----------------------------
def normalize(text):
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

# ----------------------------
# 3. Tokenisation
# ----------------------------
def tokenize(text):
    return normalize(text).split()

# ----------------------------
# 4. Distance Levenshtein sur mots (librairie)
# ----------------------------
def levenshtein_words(s1, s2, max_words=10):
    w1 = tokenize(s1)
    w2 = tokenize(s2)

    if len(w1) > max_words or len(w2) > max_words:
        return None

    # RapidFuzz accepte directement les listes
    return Levenshtein.distance(w1, w2)

# ----------------------------
# 5. Charger les données DB
# ----------------------------
def load_phrases():
    with conn.cursor() as cur:
        cur.execute("SELECT id, texte FROM phrases;")
        return cur.fetchall()

# ----------------------------
# 6. Recherche fuzzy
# ----------------------------
def search(query, max_distance=2):
    data = load_phrases()
    results = []

    for id_, texte in data:
        dist = levenshtein_words(query, texte)

        if dist is not None and dist <= max_distance:
            results.append({
                "id": id_,
                "texte": texte,
                "distance": dist
            })

    # tri
    results.sort(key=lambda x: x["distance"])
    return results

# ----------------------------
# 7. Programme principal
# ----------------------------
if __name__ == "__main__":
    print("=== Recherche Levenshtein (PostgreSQL + Python) ===")

    query = input("Entrez une phrase (max 10 mots) : ")

    results = search(query)

    print("\nRésultats :")
    if not results:
        print("Aucun résultat.")
    else:
        for r in results:
            print(f"{r['texte']} → distance = {r['distance']}")

    conn.close()
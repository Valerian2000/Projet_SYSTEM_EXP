import psycopg2
from rapidfuzz.distance import Levenshtein
from mots_francais import mots_francais_var
import mots_francais


# Connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="DB001",
    user="postgres",
    password="14062000"
)



try:
    with conn.cursor() as cur:

        # Vider la table
        cur.execute("TRUNCATE TABLE produits RESTART IDENTITY;")


        # Création de la table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id SERIAL PRIMARY KEY,
                nom TEXT
            );
        """)



        # Insertion des données
        for lettre, mots in mots_francais_var.items():
            for mot in mots:
                cur.execute(
                    "INSERT INTO produits (nom) VALUES (%s);", (mot,)
                )

        


    # Valider les changements
    conn.commit()
    print("Table créée et données insérées avec succès.")

except Exception as e:
    print("Erreur :", e)
    conn.rollback()


# Charger les données
def load_data():
    with conn.cursor() as cur:
        cur.execute("SELECT id, nom FROM produits;")
        return cur.fetchall()  # [(id, nom), ...]

def levenshtein_search(query, data):
    results = []

    for id_, word in data:

        # 
        # Filtrage rapide AVANT calcul coûteux
        if abs(len(word) - len(query)) > 2:
            continue

        if not word or not query:
            continue

        if word[0] != query[0]:
            continue

        # Calcul seulement si utile
        dist = Levenshtein.distance(query, word)
        results.append({
            "id": id_,
            "mot": word,
            "distance": dist
        })
        
    return sorted(results, key=lambda x: x["distance"])

# Programme principal
if __name__ == "__main__":

    data = load_data()
    ancienne_phrase = input("Votre phrase : ")
    mots = ancienne_phrase.split()
    nouvelle_phrase = []

    for mot in mots:
        results = levenshtein_search(mot, data)
        best_match = min(results, key=lambda x: x["distance"])
        nouvelle_phrase.append(best_match["mot"])

    print(" ".join(nouvelle_phrase))

# Fermer connexion
conn.close()
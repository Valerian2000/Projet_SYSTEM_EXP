import psycopg2
from rapidfuzz.distance import Levenshtein


# Connexion PostgreSQL
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
            CREATE TABLE IF NOT EXISTS produits (
                id SERIAL PRIMARY KEY,
                nom TEXT
            );
        """)

        # Insertion des données
        cur.execute("""
            INSERT INTO produits (nom) VALUES
            ('chat'), ('chien'), ('chats'),
            ('chaise'), ('chapeau'),
            ('voiture'), ('ordinateur');
        """)

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

# Recherche Levenshtein
def levenshtein_search(query, data, max_distance=2):
    results = []

    for id_, word in data:
        dist = Levenshtein.distance(query, word)

        if dist <= max_distance:
            results.append({
                "id": id_,
                "mot": word,
                "distance": dist
            })

    # Trier par distance croissante
    results.sort(key=lambda x: x["distance"])

    return results

# Programme principal
if __name__ == "__main__":
    data = load_data()

    query = input("Recherche : ")

    results = levenshtein_search(query, data)

    print("\nRésultats :")
    for r in results:
        print(f"{r['mot']} (distance={r['distance']})")

# Fermer connexion
conn.close()
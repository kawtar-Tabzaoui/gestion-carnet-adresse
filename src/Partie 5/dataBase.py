import sqlite3    # bibliothèque pour travailler avec SQLite (déjà installée avec Python)
import hashlib    # pour crypter les mots de passe
import csv

def conexion():

    # crée le fichier de base de données carnet.db s'il n'existe pas
    return sqlite3.connect("carnet.db")

def initialiser_bd():
    connexion = conexion() # ouvrir la connexion
    cursor = connexion.cursor() # stylo bach nktbo f BD

    # creation table contacts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nom       TEXT NOT NULL,
            email     TEXT NOT NULL,
            telephone TEXT NOT NULL
        )
    """)
    # Créer la table admins pour stocker les admins

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL,
            mot_de_passe  TEXT NOT NULL
        )
    """)

    # ajouter admin par défaut si la table vide
    cursor.execute("SELECT COUNT(*) FROM admins")# combien d'admins kayn f la table
    if cursor.fetchone()[0] == 0:# yjib résulta 0, jib premier element [0] == 0wach vide
        mot_de_passe_hache = hashlib.sha256("admin123".encode()).hexdigest() # crypter admin123
        cursor.execute(
            "INSERT INTO admins (username, mot_de_passe) VALUES (?, ?)",
            ("admin", mot_de_passe_hache)# nzido les admins f la table

        )
    connexion.commit()# sauvgarder
    connexion.close()# fermer



def ajouter_contact(nom, email, telephone):
    connexion = conexion()
    cursor = connexion.cursor()

    # vérifier doublon par NOM
    cursor.execute(
        "SELECT * FROM contacts WHERE LOWER(nom) = LOWER(?)",
        (nom,)
    )
    if cursor.fetchone():
        connexion.close()
        return False, "nom"  # ← nom existe déjà

    # vérifier doublon par EMAIL
    cursor.execute(
        "SELECT * FROM contacts WHERE LOWER(email) = LOWER(?)",
        (email,)
    )
    if cursor.fetchone():
        connexion.close()
        return False, "email"  # ← email existe déjà

    # ajouter le contact
    cursor.execute(
        "INSERT INTO contacts (nom, email, telephone) VALUES (?, ?, ?)",
        (nom, email, telephone)
    )
    connexion.commit()
    connexion.close()
    return True, None


def supprimer_contact(info):
    connexion = conexion()
    cursor = connexion.cursor()

    # chercher par nom OU email
    cursor.execute(
        """DELETE FROM contacts 
           WHERE LOWER(nom) = LOWER(?) 
           OR LOWER(email) = LOWER(?)""",
        (info, info)
    )
    rows = cursor.rowcount  # nombre de lignes supprimées
    connexion.commit()
    connexion.close()
    return rows > 0  # True si supprimé, False si pas trouvé




# afficher tous les contact
def get_all_contacts():
    connexion = conexion()
    cursor = connexion.cursor()
    cursor.execute(
        "SELECT nom, email, telephone FROM contacts ORDER BY nom" # lire les données trier par ordre alphabetique
    )
    contacts = cursor.fetchall()  # récupérer tous les lignes
    connexion.close()
    return contacts               # retourner liste des contacts


def verifier_admin(username, mot_de_passe):
    connexion = conexion()# ouvrir la bd et préparer le curseur
    cursor = connexion.cursor()

    # hacher le mot de passe entré

    mot_de_passe_hache = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    # chercher dans la table admins
    cursor.execute(
        "SELECT * FROM admins WHERE username = ? AND mot_de_passe = ?", # chercher dans la table admine
        (username, mot_de_passe_hache)
    )
    result = cursor.fetchone()  # None si pas trouvé
    connexion.close()
    return result is not None   # True si trouvé, False sinon ( identification incorrect)


def exporter_csv():
    contacts = get_all_contacts()  # récupérer tous les contacts
    with open("contacts_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f) # outil pour ecrir dans un fichier csv
        writer.writerow(["Nom", "Email", "Téléphone"])  # entête , # ecrir une ligne
        for c in contacts:
            writer.writerow(c)   # écrire chaque contact
    return "contacts_export.csv"
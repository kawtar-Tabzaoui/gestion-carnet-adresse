import sqlite3    # bibliothèque pour travailler avec SQLite (déjà installée avec Python)
import hashlib    # pour crypter les mots de passe
import csv

def conexion():
    return sqlite3.connect("carnet.db")

    # crée le fichier de base de données carnet.db s'il n'existe pas
    #import os
    #base_dir = os.path.dirname(os.path.abspath(__file__))
    #db_path = os.path.join(base_dir, "..", "src", "carnet.db")
    #return sqlite3.connect(db_path)

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
    conn = conexion()
    cursor = conn.cursor()

    try:
        id = int(info)
        cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
    except ValueError:
        cursor.execute(
            """DELETE FROM contacts 
               WHERE LOWER(nom) = LOWER(?) 
               OR LOWER(email) = LOWER(?)""",
            (info, info)
        )
    rows = cursor.rowcount
    conn.commit()
    conn.close()
    return rows > 0





# afficher tous les contact
def get_all_contacts():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email, telephone FROM contacts ORDER BY nom")
    contacts = cursor.fetchall()
    conn.close()
    return contacts


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


def modifier_contact(id, nom, email, telephone):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contacts SET nom=?, email=?, telephone=? WHERE id=?",
        (nom, email, telephone, id)
    )
    conn.commit()
    conn.close()


def exporter_csv():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email, telephone FROM contacts ORDER BY nom")
    contacts = cursor.fetchall()
    conn.close()
    with open("contacts_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nom", "Email", "Téléphone"])
        for c in contacts:
            writer.writerow([c[0], c[1], c[2], c[3]])
    return "contacts_export.csv"
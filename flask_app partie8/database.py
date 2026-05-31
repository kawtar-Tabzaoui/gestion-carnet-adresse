import sqlite3
import hashlib
import csv


def conexion():
    return sqlite3.connect("carnet.db")


def initialiser_bd():
    connexion = conexion()
    cursor = connexion.cursor()

    # TABLE CONTACTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            telephone TEXT NOT NULL,
            categorie TEXT,
            adresse TEXT,
            fonction TEXT,
            entreprise TEXT
        )
    """)

    # TABLE ADMINS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            mot_de_passe TEXT NOT NULL
        )
    """)

    # ADMIN PAR DEFAUT
    cursor.execute("SELECT COUNT(*) FROM admins")

    if cursor.fetchone()[0] == 0:
        mot_de_passe_hache = hashlib.sha256(
            "admin123".encode()
        ).hexdigest()

        cursor.execute(
            "INSERT INTO admins (username, mot_de_passe) VALUES (?, ?)",
            ("admin", mot_de_passe_hache)
        )

    connexion.commit()
    connexion.close()


def ajouter_contact(
        nom,
        email,
        telephone,
        categorie,
        adresse,
        fonction,
        entreprise
):

    connexion = conexion()
    cursor = connexion.cursor()

    # VERIFIER DOUBLON NOM
    cursor.execute(
        "SELECT * FROM contacts WHERE LOWER(nom)=LOWER(?)",
        (nom,)
    )

    if cursor.fetchone():
        connexion.close()
        return False, "nom"

    # VERIFIER DOUBLON EMAIL
    cursor.execute(
        "SELECT * FROM contacts WHERE LOWER(email)=LOWER(?)",
        (email,)
    )

    if cursor.fetchone():
        connexion.close()
        return False, "email"

    # INSERT
    cursor.execute("""
        INSERT INTO contacts (
            nom,
            email,
            telephone,
            categorie,
            adresse,
            fonction,
            entreprise
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nom,
        email,
        telephone,
        categorie,
        adresse,
        fonction,
        entreprise
    ))

    connexion.commit()
    connexion.close()

    return True, None


def supprimer_contact(info):

    conn = conexion()
    cursor = conn.cursor()

    try:
        id = int(info)

        cursor.execute(
            "DELETE FROM contacts WHERE id=?",
            (id,)
        )

    except ValueError:

        cursor.execute("""
            DELETE FROM contacts
            WHERE LOWER(nom)=LOWER(?)
            OR LOWER(email)=LOWER(?)
        """, (info, info))

    rows = cursor.rowcount

    conn.commit()
    conn.close()

    return rows > 0


def get_all_contacts():

    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        id,
        nom,
        email,
        telephone,
        categorie,
        adresse,
        fonction,
        entreprise
        FROM contacts
        ORDER BY nom
    """)

    contacts = cursor.fetchall()

    conn.close()

    return contacts


def verifier_admin(username, mot_de_passe):

    connexion = conexion()
    cursor = connexion.cursor()

    mot_de_passe_hache = hashlib.sha256(
        mot_de_passe.encode()
    ).hexdigest()

    cursor.execute(
        """
        SELECT * FROM admins
        WHERE username=?
        AND mot_de_passe=?
        """,
        (username, mot_de_passe_hache)
    )

    result = cursor.fetchone()

    connexion.close()

    return result is not None


def modifier_contact(
        id,
        nom,
        email,
        telephone,
        categorie,
        adresse,
        fonction,
        entreprise
):

    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE contacts
        SET
        nom=?,
        email=?,
        telephone=?,
        categorie=?,
        adresse=?,
        fonction=?,
        entreprise=?
        WHERE id=?
    """, (
        nom,
        email,
        telephone,
        categorie,
        adresse,
        fonction,
        entreprise,
        id
    ))

    conn.commit()
    conn.close()


def exporter_csv():

    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        id,
        nom,
        email,
        telephone,
        categorie,
        adresse,
        fonction,
        entreprise
        FROM contacts
        ORDER BY nom
    """)

    contacts = cursor.fetchall()

    conn.close()

    with open(
            "contacts_export.csv",
            "w",
            newline="",
            encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "ID",
            "Nom",
            "Email",
            "Téléphone",
            "Catégorie",
            "Adresse",
            "Fonction",
            "Entreprise"
        ])

        for c in contacts:
            writer.writerow(c)

    return "contacts_export.csv"
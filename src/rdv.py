import sqlite3
from datetime import datetime, timedelta

DB_FILE = "rdv.db"

def conexion():
    return sqlite3.connect(DB_FILE)

def initialiser_rdv():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rdv (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            heure TEXT NOT NULL,
            nom_patient TEXT NOT NULL,
            motif TEXT DEFAULT '',
            statut TEXT DEFAULT 'réservé'
        )
    """)
    conn.commit()
    conn.close()

def get_creneaux(date):
    creneaux = []
    debut = datetime.strptime("08:00", "%H:%M")
    fin = datetime.strptime("18:00", "%H:%M")
    while debut < fin:
        creneaux.append(debut.strftime("%H:%M"))
        debut += timedelta(minutes=30)
    return creneaux

def reserver_rdv(date, heure, nom_patient, motif):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM rdv WHERE date=? AND heure=?",
        (date, heure)
    )
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute(
        "INSERT INTO rdv (date, heure, nom_patient, motif, statut) VALUES (?, ?, ?, ?, ?)",
        (date, heure, nom_patient, motif, "réservé")
    )
    conn.commit()
    conn.close()
    return True

def get_rdv_par_date(date):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT heure, nom_patient, motif, statut FROM rdv WHERE date=?",
        (date,)
    )
    rdvs = cursor.fetchall()
    conn.close()
    return rdvs

def annuler_rdv(date, heure):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM rdv WHERE date=? AND heure=?",
        (date, heure)
    )
    conn.commit()
    conn.close()

def get_all_rdv():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rdv ORDER BY date, heure")
    rdvs = cursor.fetchall()
    conn.close()
    return rdvs
import sqlite3
import csv
import os

conn = sqlite3.connect("carnet.db")
cursor = conn.cursor()

cursor.execute("SELECT id, username, mot_de_passe FROM admins")
admins = cursor.fetchall()

with open("voir_admins.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Username", "Mot de passe hashé"])
    writer.writerows(admins)

conn.close()

os.startfile("voir_admins.csv")
print("✅ voir_admins.csv créé !")
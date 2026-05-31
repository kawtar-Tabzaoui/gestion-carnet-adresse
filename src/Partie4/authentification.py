import hashlib  # bibliothèque pour hacher (crypter) les mots de passe
import json     # pour sauvegarder les admins dans un fichier
import os       # pour vérifier si le fichier existe

ADMIN_FILE = "admins.json"  # nom du fichier qui stocke les admins

def hacher_mot_de_passe(mot_de_passe):
    # transforme "admin123" → "a665a45920..." (impossible à lire)
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()

def initialiser_admin():
    # si le fichier admins.json n'existe pas → le créer avec admin par défaut
    if not os.path.exists(ADMIN_FILE):
        admin_defaut = {
            "admin": hacher_mot_de_passe("admin123")
        }
        with open(ADMIN_FILE, "w") as f:
            json.dump(admin_defaut, f)

def verifier_admin(username, mot_de_passe):
    # vérifier si username + mot_de_passe sont corrects
    initialiser_admin()  # créer le fichier si inexistant
    with open(ADMIN_FILE, "r") as f:
        admins = json.load(f)  # lire les admins
    # hacher le mot de passe entré et comparer
    return admins.get(username) == hacher_mot_de_passe(mot_de_passe)
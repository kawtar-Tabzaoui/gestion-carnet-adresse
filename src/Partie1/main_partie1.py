from contact_partie1 import Contact
from address_book_partie1 import Adress_book
import re

def menu():
    # Instanciation du carnet d'adresses
    mon_carnet = Adress_book()

    while True:
        print("\n--- Notre Menu d'Adresses ---")
        print("1. Ajouter Contact")
        print("2. Supprimer Contact")
        print("3. Afficher Contacts")
        print("4. Quitter")

        choix = input("Choisissez une option (1-4) : ")

        # Correction : utilisation de "1" en tant que chaîne de caractères
        if choix == "1":
            nom = input("Nom : ")
            while True:
                if isinstance(nom, str) and len(nom) > 0:
                    break
                else:
                    print("le nom n'est pas valide")
                    nom = input("Entrer s'il vous plait votre nom:")





            email = input("Email : ")
            while True:
                email_structure = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if re.match(email_structure, email):
                    break
                else:
                    print("Email non valide")
                    email =input("Erreur S'il vous plait entrer votre email:")





            telephone = input("Téléphone : ")
            while True:
                if telephone.isdigit() and len(telephone) == 10:
                    break
                else:
                    print("Telephone non valide")
                    telephone = input("Erreur S'il vous plait votre telephone:")



            try:
                # Création de l'objet et ajout au carnet
                nouveau_contact = Contact(nom, email, telephone)
                mon_carnet.ajouter_contact(nouveau_contact)
            except AssertionError as e:
                # Gestion des erreurs soulevées par les asserts
                print(f"Erreur de validation : {e}")

        elif choix == "2":
            nom_a_supprimer = input("Entrez le nom ou Email du contact à supprimer : ")# nom ou email à supprimer
            mon_carnet.supprimer_contact(nom_a_supprimer)

        elif choix == "3":
            mon_carnet.afficher_contactes()

        elif choix == "4":
            print("Fermeture du programme. Au revoir !")
            break

        else:
            print("Option invalide, veuillez réessayer.")


if __name__ == "__main__":
    menu()

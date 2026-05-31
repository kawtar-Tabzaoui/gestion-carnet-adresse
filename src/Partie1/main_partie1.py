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
            assert isinstance(nom, str) and len(nom) > 0, "Nom non valide"

            email = input("Email : ")
            emai_structure = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            assert re.match(emai_structure, email), "Email non valide"

            telephone = input("Téléphone : ")
            assert telephone.isdigit() and len(telephone) == 10, "Telephone non valide"

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
from contact_partie1 import Contact
import re


class Adress_book:
    def __init__(self):
        self.contacts = []

    def ajouter_contact(self, nouveau_contact):
        # # les condition pour email
        assert isinstance(nouveau_contact.email, str) and len(nouveau_contact.email) > 0, "email non valide"
        emai_structure = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        assert re.match(emai_structure, nouveau_contact.email), "email non valide"

        # conditions pour telephone
        assert nouveau_contact.telephone.isdigit() and len(nouveau_contact.telephone) == 10, "telephone non valide"

        # contacte deja ajouter
        for contact in self.contacts:
            if contact.nom.lower() == nouveau_contact.nom.lower():
                print("Ce contact existe déjà.")
                return

        # Ajout contact
        self.contacts.append(nouveau_contact)
        print("Le contact est ajouté.")

    def supprimer_contact(self, info):
        # info : peut être soit le nom, soit l'email
        for c in self.contacts:
            # On vérifie si l'info correspond au nom OU à l'email
            if c.nom.lower() == info.lower() or c.email.lower() == info.lower():
                self.contacts.remove(c)
                print(f"Contact {info} supprimé avec succès.")
                return # On sort de la fonction dès qu'on trouve le contact

        # Si la boucle se termine sans rien trouver
        print("Aucun contact trouvé avec ce nom ou cet email.")

    def afficher_contactes(self):
        if not self.contacts:
            print("Le carnet est vide.")
        else:
            print("---------- Liste des contacts ----------")
            for i, contact in enumerate(self.contacts, 1):
                # Corrected: using .nom, .email, and .telephone
                print(f"{i}. {contact.nom} | {contact.email} | {contact.telephone}")
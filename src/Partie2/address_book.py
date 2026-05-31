from contact import Contact
import re
import os

class Adress_book:
    def __init__(self,fichier="contacts.txt"):
        self.fichier = fichier
        if not os.path.exists(self.fichier):
            open(self.fichier, "w").close()



    def ajouter_contact(self, nouveau_contact):
        contacts = self.get_all_contacts()
        # # les condition pour email
        assert isinstance(nouveau_contact.email, str) and len(nouveau_contact.email) > 0, "email non valide"
        emai_structure = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        assert re.match(emai_structure, nouveau_contact.email), "email non valide"

        # conditions pour telephone
        assert nouveau_contact.telephone.isdigit() and len(nouveau_contact.telephone) == 10, "telephone non valide"

        # contacte deja ajouter
        for contact in contacts:
            if contact.nom.lower() == nouveau_contact.nom.lower():
                print("Ce contact existe déjà.")
                return

        # Ajouter le contact à la fin du fichier (mode "a" pour append)
        with open(self.fichier, "a") as f:
            f.write(f"{nouveau_contact.nom},{nouveau_contact.email},{nouveau_contact.telephone}\n")
        return True

    def get_all_contacts(self):
        contacts= []
        with open(self.fichier, "r") as f:
            for ligne in f:
                nom,email,telephone = ligne.strip().split(",")
                contacts.append(Contact(nom,email,telephone))
        return contacts


    #def display_contacts(self):
     #   """Affiche tous les contacts du carnet."""
     #   contacts = self.get_all_contacts()
      #  if not contacts:
      #      print("Aucun contact")
       # else:
            #for c in contacts:
                # On utilise ici la méthode __str__ de la classe Contact
              #  print(c)

    def supprimer_contact(self, nom):
        """Supprime un contact par son nom (insensible à la casse)."""
        contacts = self.get_all_contacts()
        new_contacts = []
        found = False

        # Filtrer la liste : on garde tout sauf le nom à supprimer
        for c in contacts:
            if c.nom.lower() != nom.lower():
                new_contacts.append(c)
            else:
                found = True


        # Réécrire le fichier avec la nouvelle liste (mode "w")
        with open(self.fichier, "w") as f:
            for c in new_contacts:
                f.write(f"{c.nom},{c.email},{c.telephone}\n")

        if found:
            print(f"Contact {nom} supprimé.")
        else:
            print("Contact non trouvé.")

    def afficher_contactes(self):
        contacts = self.get_all_contacts()

        if not contacts:
            print("Le carnet est vide.")
        else:
            print("---------- Liste des contacts ----------")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact.nom} | {contact.email} | {contact.telephone}")
import tkinter as tk
from tkinter import messagebox
from contact import Contact
from address_book import Adress_book
from login import lancer_login

def lancer_application():

    root = tk.Tk()
    root.title("Carnet d'Adresses")
    root.geometry("500x500")

    carnet = Adress_book()

    # ZONE HAUT : Titre
    frame_haut = tk.Frame(root, bg="#4a90d9", pady=10)
    frame_haut.pack(fill="x")

    tk.Label(
        frame_haut,
        text="📒 Carnet d'Adresses",
        font=("Arial", 16, "bold"),
        bg="#4a90d9",
        fg="white"
    ).pack()

    # ZONE MILIEU : Listbox
    frame_milieu = tk.Frame(root, pady=10)
    frame_milieu.pack(fill="both", expand=True, padx=10)

    listbox = tk.Listbox(
        frame_milieu,
        font=("Arial", 11),
        selectbackground="#4a90d9",
        height=12
    )
    listbox.pack(fill="both", expand=True)

    # FONCTION : afficher les contacts
    def afficher_contacts():
        listbox.delete(0, tk.END)
        contacts = carnet.get_all_contacts()
        contacts = sorted(contacts, key=lambda c: c.nom.lower())
        if not contacts:
            listbox.insert(tk.END, "Aucun contact.")
        else:
            for c in contacts:
                listbox.insert(tk.END, f"{c.nom} | {c.email} | {c.telephone}")

    afficher_contacts()

    # FONCTION : ajouter un contact (popup)
    def fenetre_ajouter():
        popup = tk.Toplevel(root)
        popup.title("Ajouter un Contact")
        popup.geometry("300x220")

        tk.Label(popup, text="Nom :").pack(pady=(15, 0))
        entry_nom = tk.Entry(popup, width=30)
        entry_nom.pack()

        tk.Label(popup, text="Email :").pack(pady=(10, 0))
        entry_email = tk.Entry(popup, width=30)
        entry_email.pack()

        tk.Label(popup, text="Téléphone :").pack(pady=(10, 0))
        entry_tel = tk.Entry(popup, width=30)
        entry_tel.pack()

        def confirmer():
            nom = entry_nom.get().strip()
            email = entry_email.get().strip()
            telephone = entry_tel.get().strip()
            try:
                nouveau = Contact(nom, email, telephone)
                result = carnet.ajouter_contact(nouveau)
                if result:
                    messagebox.showinfo("Succès", f"Contact '{nom}' ajouté !")
                    popup.destroy()
                    afficher_contacts()
                else:
                    messagebox.showwarning("Attention", f"Le contact '{nom}' existe déjà !")
            except AssertionError as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(popup, text="✅ Confirmer", command=confirmer).pack(pady=15)

    # FONCTION : supprimer un contact
    def supprimer():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un contact à supprimer.")
            return
        ligne = listbox.get(selection[0])
        nom = ligne.split("|")[0].strip()
        reponse = messagebox.askyesno("Confirmation", f"Supprimer '{nom}' ?")
        if reponse:
            carnet.supprimer_contact(nom)
            afficher_contacts()

    # ZONE BAS : Boutons
    frame_bas = tk.Frame(root, pady=10)
    frame_bas.pack(fill="x", padx=10)

    tk.Button(
        frame_bas,
        text="➕ Ajouter",
        width=14,
        command=fenetre_ajouter
    ).pack(side="left", padx=5)

    tk.Button(
        frame_bas,
        text="🗑 Supprimer",
        width=14,
        command=supprimer
    ).pack(side="left", padx=5)

    tk.Button(
        frame_bas,
        text="🔄 Actualiser",
        width=14,
        command=afficher_contacts
    ).pack(side="left", padx=5)

    root.mainloop()

# LANCER LOGIN D'ABORD
lancer_login(lancer_application)
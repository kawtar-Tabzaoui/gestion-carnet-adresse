import tkinter as tk
from tkinter import messagebox
from contact import Contact
from address_book import Adress_book
from login import lancer_login


# FONCTION PRINCIPALE (kol le code dakhel hna)

def lancer_application():

    root = tk.Tk()
    root.title("Allo !")
    root.geometry("350x450")

    carnet = Adress_book()


    # ZONE HAUT : Nom + Tel + Bouton Effacer

    frame_haut = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_haut.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_haut, text="Nom :", width=5, anchor="w").grid(row=0, column=0, pady=5)
    entry_nom = tk.Entry(frame_haut, width=30)
    entry_nom.grid(row=0, column=1, pady=5)

    tk.Label(frame_haut, text="Tel :", width=5, anchor="w").grid(row=1, column=0, pady=5)
    entry_tel = tk.Entry(frame_haut, width=30)
    entry_tel.grid(row=1, column=1, pady=5)

    def effacer():
        entry_nom.delete(0, tk.END)
        entry_tel.delete(0, tk.END)

    tk.Button(frame_haut, text="Effacer", command=effacer).grid(row=2, column=1, pady=5)

    # ZONE MILIEU : Listbox + Scrollbar

    frame_milieu = tk.Frame(root, bd=2, relief="groove")
    frame_milieu.pack(fill="both", expand=True, padx=10)

    scrollbar = tk.Scrollbar(frame_milieu)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(
        frame_milieu,
        font=("Arial", 11),
        yscrollcommand=scrollbar.set
    )
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    def selectionner(event):
        selection = listbox.curselection()
        if selection:
            ligne = listbox.get(selection[0])
            parties = ligne.split("|")
            entry_nom.delete(0, tk.END)
            entry_nom.insert(0, parties[0].strip())
            entry_tel.delete(0, tk.END)
            entry_tel.insert(0, parties[2].strip())

    listbox.bind("<<ListboxSelect>>", selectionner)


    # FONCTION : afficher les contacts

    def afficher_contacts():
        listbox.delete(0, tk.END)
        contacts = sorted(carnet.get_all_contacts(), key=lambda c: c.nom.lower())
        if not contacts:
            listbox.insert(tk.END, "Aucun contact.")
        else:
            for c in contacts:
                listbox.insert(tk.END, f"{c.nom} | {c.email} | {c.telephone}")

    afficher_contacts()


    # FONCTION : ajouter un contact

    def ajouter():
        nom = entry_nom.get().strip()
        tel = entry_tel.get().strip()

        popup = tk.Toplevel(root)
        popup.title("Email")
        popup.geometry("280x120")
        tk.Label(popup, text="Email :").pack(pady=10)
        entry_email = tk.Entry(popup, width=30)
        entry_email.pack()

        def confirmer():
            email = entry_email.get().strip()
            try:
                nouveau = Contact(nom, email, tel)
                result = carnet.ajouter_contact(nouveau)
                if result:
                    messagebox.showinfo("Succès", f"Contact '{nom}' ajouté !")
                    popup.destroy()
                    afficher_contacts()
                    effacer()
                else:
                    messagebox.showwarning("Attention", f"le contact '{nom}' existe déjà")
            except AssertionError as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(popup, text="✅ Confirmer", command=confirmer).pack(pady=10)


    # FONCTION : supprimer un contact

    def supprimer():
        nom = entry_nom.get().strip()
        if not nom:
            messagebox.showwarning("Attention", "Sélectionnez un contact d'abord !")
            return
        reponse = messagebox.askyesno("Confirmation", f"Supprimer '{nom}' ?")
        if reponse:
            carnet.supprimer_contact(nom)
            afficher_contacts()
            effacer()

    # ZONE BAS : Boutons
    frame_bas = tk.Frame(root, pady=10)
    frame_bas.pack(fill="x", padx=10)

    tk.Button(frame_bas, text="Ajouter",   width=10, command=ajouter).pack(side="left", padx=5)
    tk.Button(frame_bas, text="Supprimer", width=10, command=supprimer).pack(side="left", padx=5)
    tk.Button(frame_bas, text="Afficher",  width=10, command=afficher_contacts).pack(side="left", padx=5)

    root.mainloop()


# LANCER LOGIN D'ABORD
lancer_login(lancer_application)




















#root.mainloop()
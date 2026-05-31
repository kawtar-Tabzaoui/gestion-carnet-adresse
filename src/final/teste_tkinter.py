import tkinter as tk
from tkinter import messagebox
from contact import Contact
from dataBase import ajouter_contact,supprimer_contact, get_all_contacts, verifier_admin, exporter_csv
from login import lancer_login


# FONCTION PRINCIPALE (kol le code dakhel hna)

def lancer_application():

    root = tk.Tk()
    root.title("Carnet d'addresse !")
    root.geometry("350x450")



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
        contacts = get_all_contacts()  # ← men SQLite direct
        if not contacts:
            listbox.insert(tk.END, "Aucun contact.")
        else:
            for c in contacts:
                # c = (nom, email, telephone)
                listbox.insert(tk.END, f"{c[0]} | {c[1]} | {c[2]}")

    afficher_contacts()


    # FONCTION : ajouter un contact

    def ajouter():
        popup = tk.Toplevel(root)
        popup.title("Ajouter un contact")
        popup.geometry("300x230")
        popup.resizable(False, False)

        tk.Label(popup, text="Ajouter un contact",
                 font=("Arial", 11, "bold")).pack(pady=10)

        # Nom
        frame_n = tk.Frame(popup)
        frame_n.pack(pady=3)
        tk.Label(frame_n, text="Nom :", width=12, anchor="w").pack(side="left")
        entry_nom_p = tk.Entry(frame_n, width=20)
        entry_nom_p.pack(side="left")

        # Email
        frame_e = tk.Frame(popup)
        frame_e.pack(pady=3)
        tk.Label(frame_e, text="Email :", width=12, anchor="w").pack(side="left")
        entry_email_p = tk.Entry(frame_e, width=20)
        entry_email_p.pack(side="left")

        # Téléphone
        frame_t = tk.Frame(popup)
        frame_t.pack(pady=3)
        tk.Label(frame_t, text="Téléphone :", width=12, anchor="w").pack(side="left")
        entry_tel_p = tk.Entry(frame_t, width=20)
        entry_tel_p.pack(side="left")

        def confirmer():
            nom = entry_nom_p.get().strip()
            email = entry_email_p.get().strip()
            tel = entry_tel_p.get().strip()

            try:
                # valider avec Contact()
                Contact(nom, email, tel)

                # ajouter dans SQLite
                result, doublon = ajouter_contact(nom, email, tel)
                if result:
                    messagebox.showinfo("Succès", f"Contact '{nom}' ajouté !")
                    popup.destroy()
                    afficher_contacts()
                else:
                    if doublon == "nom":
                        messagebox.showwarning("Attention",
                                               f"Le nom '{nom}' existe déjà !")
                    else:
                        messagebox.showwarning("Attention",
                                               f"L'email '{email}' existe déjà !")
            except AssertionError as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(popup, text="✅ Confirmer",
                  command=confirmer, width=15).pack(pady=10)
    # FONCTION : supprimer un contact

    def supprimer():
        # popup pour entrer nom ou email
        popup = tk.Toplevel(root)
        popup.title("Supprimer un contact")
        popup.geometry("300x150")
        popup.resizable(False, False)

        tk.Label(popup, text="Supprimer un contact",
                 font=("Arial", 11, "bold")).pack(pady=10)

        frame = tk.Frame(popup)
        frame.pack(pady=5)
        tk.Label(frame, text="Nom ou Email :", width=13, anchor="w").pack(side="left")
        entry_info = tk.Entry(frame, width=20)
        entry_info.pack(side="left")

        def confirmer_suppr():
            info = entry_info.get().strip()
            if not info:
                messagebox.showwarning("Attention", "Entrez un nom ou email !")
                return
            reponse = messagebox.askyesno("Confirmation",
                                          f"Supprimer '{info}' ?")
            if reponse:
                result = supprimer_contact(info)
                if result:
                    messagebox.showinfo("Succès", f"Contact '{info}' supprimé !")
                    popup.destroy()
                    afficher_contacts()
                    effacer()
                else:
                    messagebox.showerror("Erreur",
                                         f"Contact '{info}' non trouvé !")

        tk.Button(popup, text="🗑️ Supprimer",
                  command=confirmer_suppr, width=15).pack(pady=10)

    def exporter():
        fichier = exporter_csv()  # ← exporter men SQLite
        messagebox.showinfo("Succès",
                            f"Contacts exportés dans '{fichier}' !")

    # ZONE BAS : Boutons
    frame_bas = tk.Frame(root, pady=10)
    frame_bas.pack(fill="x", padx=10)

    tk.Button(frame_bas, text="Ajouter", width=8, command=ajouter).pack(side="left", padx=3)
    tk.Button(frame_bas, text="Supprimer", width=8, command=supprimer).pack(side="left", padx=3)
    tk.Button(frame_bas, text="Afficher", width=8, command=afficher_contacts).pack(side="left", padx=3)
    tk.Button(frame_bas, text="Export CSV", width=8, command=exporter).pack(side="left", padx=3)
    root.mainloop()


# LANCER LOGIN D'ABORD
lancer_login(lancer_application)




















#root.mainloop()
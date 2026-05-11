import tkinter as tk
from tkinter import messagebox
from contact import Contact
from address_book import Adress_book

root = tk.Tk()
root.title("Allo !")                      # smiya dyal la fenêtre
root.geometry("350x450")                  # taille dyal la fenêtre

carnet = Adress_book()                    # créer le carnet

# ════════════════════════════════════════════════════
# ZONE HAUT : Nom + Tel + Bouton Effacer
# ════════════════════════════════════════════════════
frame_haut = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)  # bd=bordure, relief=style bordure
frame_haut.pack(fill="x", padx=10, pady=10)                           # afficher zone haut

# ── Ligne Nom ─────────────────────────────────────
tk.Label(frame_haut, text="Nom :", width=5, anchor="w").grid(row=0, column=0, pady=5)  # label Nom
entry_nom = tk.Entry(frame_haut, width=30)                             # champ saisie nom
entry_nom.grid(row=0, column=1, pady=5)                                # placer f ligne 0

# ── Ligne Tel ─────────────────────────────────────
tk.Label(frame_haut, text="Tel :", width=5, anchor="w").grid(row=1, column=0, pady=5)  # label Tel
entry_tel = tk.Entry(frame_haut, width=30)                             # champ saisie tel
entry_tel.grid(row=1, column=1, pady=5)                                # placer f ligne 1

# ── Bouton Effacer ────────────────────────────────
def effacer():
    entry_nom.delete(0, tk.END)           # hyed le texte men champ nom
    entry_tel.delete(0, tk.END)           # hyed le texte men champ tel

tk.Button(frame_haut, text="Effacer", command=effacer).grid(row=2, column=1, pady=5)  # bouton effacer

# ════════════════════════════════════════════════════
# ZONE MILIEU : Listbox + Scrollbar
# ════════════════════════════════════════════════════
frame_milieu = tk.Frame(root, bd=2, relief="groove")     # créer zone milieu avec bordure
frame_milieu.pack(fill="both", expand=True, padx=10)     # afficher zone milieu

scrollbar = tk.Scrollbar(frame_milieu)                   # créer scrollbar
scrollbar.pack(side="right", fill="y")                   # mettre scrollbar f droite

listbox = tk.Listbox(
    frame_milieu,
    font=("Arial", 11),
    yscrollcommand=scrollbar.set          # relier listbox m3a scrollbar
)
listbox.pack(fill="both", expand=True)   # afficher listbox
scrollbar.config(command=listbox.yview)  # relier scrollbar m3a listbox

# ── Mnin tclick f contact f listbox, tban f les champs ──
def selectionner(event):
    selection = listbox.curselection()    # jib l'index dyal contact selectionné
    if selection:
        ligne = listbox.get(selection[0]) # jib le texte dyal la ligne
        parties = ligne.split("|")        # qssem b |
        entry_nom.delete(0, tk.END)       # hyed le texte l9dim
        entry_nom.insert(0, parties[0].strip())  # affich le nom f champ
        entry_tel.delete(0, tk.END)       # hyed le texte l9dim
        entry_tel.insert(0, parties[2].strip())  # affich le tel f champ

listbox.bind("<<ListboxSelect>>", selectionner)  # relier l'event selection m3a fonction

# ════════════════════════════════════════════════════
# FONCTION : afficher les contacts
# ════════════════════════════════════════════════════
def afficher_contacts():
    listbox.delete(0, tk.END)             # hyed kol li kayn
    contacts = sorted(carnet.get_all_contacts(), key=lambda c: c.nom.lower())  # rتب alphabétiquement
    if not contacts:
        listbox.insert(tk.END, "Aucun contact.")
    else:
        for c in contacts:
            listbox.insert(tk.END, f"{c.nom} | {c.email} | {c.telephone}")  # affich kol contact

afficher_contacts()                       # afficher au démarrage

# ════════════════════════════════════════════════════
# FONCTION : ajouter un contact
# ════════════════════════════════════════════════════
def ajouter():
    nom = entry_nom.get().strip()         # jib le nom men champ
    tel = entry_tel.get().strip()         # jib le tel men champ
    email = ""                            # email mabانش f interface - nطلبوه b popup

    # popup bach yدخل email
    popup = tk.Toplevel(root)
    popup.title("Email")
    popup.geometry("280x120")
    tk.Label(popup, text="Email :").pack(pady=10)
    entry_email = tk.Entry(popup, width=30)
    entry_email.pack()

    def confirmer():
        email = entry_email.get().strip()  # jib email
        try:
            nouveau = Contact(nom, email, tel)       # créer contact - kayvalidiwi
            result = carnet.ajouter_contact(nouveau) # ajouter f fichier
            if result:
                messagebox.showinfo("Succès", f"Contact '{nom}' ajouté !")
                popup.destroy()           # sfer popup
                afficher_contacts()       # refresh listbox
                effacer()                 # hyed les champs
            else:
                messagebox.showwarning("Attention", f"le contatct'{nom}' existe déja")
        except AssertionError as e:
            messagebox.showerror("Erreur", str(e))

    tk.Button(popup, text="✅ Confirmer", command=confirmer).pack(pady=10)

# ════════════════════════════════════════════════════
# FONCTION : supprimer un contact
# ════════════════════════════════════════════════════
def supprimer():
    nom = entry_nom.get().strip()         # jib le nom men champ
    if not nom:
        messagebox.showwarning("Attention", "Sélectionnez un contact d'abord !")
        return
    reponse = messagebox.askyesno("Confirmation", f"Supprimer '{nom}' ?")  # confirmation
    if reponse:
        carnet.supprimer_contact(nom)     # supprimer men fichier
        afficher_contacts()               # refresh listbox
        effacer()                         # hyed les champs

# ════════════════════════════════════════════════════
# ZONE BAS : Boutons
# ════════════════════════════════════════════════════
frame_bas = tk.Frame(root, pady=10)       # créer zone bas
frame_bas.pack(fill="x", padx=10)        # afficher zone bas

tk.Button(frame_bas, text="Ajouter",    width=10, command=ajouter).pack(side="left", padx=5)   # bouton ajouter
tk.Button(frame_bas, text="Supprimer",  width=10, command=supprimer).pack(side="left", padx=5) # bouton supprimer
tk.Button(frame_bas, text="Afficher",   width=10, command=afficher_contacts).pack(side="left", padx=5) # bouton afficher

root.mainloop()                           # lancer la fenêtre

































#import tkinter as tk
#from tkinter import messagebox  # import séparé !
# 1. Créer la fenêtre principale
root = tk.Tk()
# 2. Titre de la fenêtre
#root.title("Notre Aplication")
# 3. Taille de la fenêtre (largeur x hauteur)
#root.geometry("400x300")


# ── 3 types de popups ─────────────────────────────────

#def popup_info():
 #   messagebox.showinfo("Succès", "Contact ajouté avec succès !")

#def popup_erreur():
#    messagebox.showerror("Erreur", "Email non valide !")

#def popup_confirmation():
 #   reponse = messagebox.askyesno("Confirmation", "Voulez-vous supprimer ce contact ?")
  #  if reponse:
    #    print("OUI → supprimer")
    #else:
     #   print("NON → annuler")

# ── Boutons ───────────────────────────────────────────
#tk.Button(root, text=" Info",          command=popup_info,         width=20).pack(pady=10)
#tk.Button(root, text=" Erreur",        command=popup_erreur,       width=20).pack(pady=10)
#tk.Button(root, text=" Confirmation",  command=popup_confirmation, width=20).pack(pady=10)
# ── Frame + Listbox ───────────────────────────────────
#frame = tk.Frame(root)
#frame.pack(fill="both", expand=True, padx=10, pady=10)

#listbox = tk.Listbox(frame, font=("Arial", 12), height=8)
#listbox.pack(fill="both", expand=True)

# Ajouter des éléments dans la Listbox
#listbox.insert(tk.END, "Alice | alice@gmail.com | 0612345678")
#listbox.insert(tk.END, "Bob   | bob@gmail.com   | 0698765432")
#listbox.insert(tk.END, "Youssef | youssef@gmail.com | 0611223344")

# ── Bouton pour voir l'élément sélectionné ────────────
#def voir_selection():
 #   selection = listbox.curselection()  # retourne l'index sélectionné
  #  if selection:
   #     ligne = listbox.get(selection[0])  # récupérer le texte
    #    print("Sélectionné :", ligne)
    #else:
     #   print("Rien sélectionné !")

#tk.Button(root, text="Voir sélection", command=voir_selection).pack(pady=10)

root.mainloop()
# ── Frame du HAUT (zone supérieure)
#frame_haut = tk.Frame(root, bg="blue", height=60)
#frame_haut.pack(fill="x")  # fill="x" = s'étirer en largeur


#tk.Label(frame_haut, text="Zone HAUT", bg="blue", fg="white",
 #        font=("Arial", 14)).pack(pady=15)


# ── Frame du MILIEU
#frame_milieu = tk.Frame(root, bg="lightgray")
#frame_milieu.pack(fill="both", expand=True)  # expand=True = prendre le max d'espace

#tk.Label(frame_milieu, text="Zone MILIEU", bg="lightgray",
 #        font=("Arial", 14)).pack(pady=40)

# ── Frame du BAS
#frame_bas = tk.Frame(root, bg="green", height=60)
#frame_bas.pack(fill="x")

#tk.Label(frame_bas, text="Zone BAS", bg="green", fg="white",
 #        font=("Arial", 14)).pack(pady=15)


# Fonction qui s'exécute quand on clique
#def cliquer():
 #   print("Bouton cliqué !")

#def afficher():
 #   texte = entry.get()       # récupérer ce que l'utilisateur a tapé
  #  print("Tu as tapé :", texte)

#tk.Label(root, text="Ton nom :").pack(pady=10)
#entry = tk.Entry(root, width=30)
#entry.pack()
#tk.Button(root, text="Afficher", command=afficher).pack(pady=10)

# Label = zone de texte
#label = tk.Label(root, text="Bonjour", font=("Arial", 25))
#label.pack(pady=20)# placer l'elelement dans la fenetre

#bouton = tk.Button(root, text="Cliqué ici", command=cliquer)
#bouton.pack()
# 4. Lancer la fenêtre (toujours à la fin !)
root.mainloop()
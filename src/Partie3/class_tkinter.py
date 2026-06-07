import tkinter as tk                      # imported tkinter - bibliothèque dyal les fenêtres
from tkinter import messagebox            # imported messagebox - bach naffcho les popups
from contact import Contact               # imported classe Contact dyal partie1
from address_book import Adress_book      # imported classe Adress_book dyal partie2

# ── Fenêtre principale ────────────────────────────────
root = tk.Tk()                            # créer la fenêtre principale
root.title("Carnet d'Adresses")          # smiya dyal la fenêtre
root.geometry("500x500")                  # taille dyal la fenêtre (largeur x hauteur)

carnet = Adress_book()                    # créer le carnet - kayqra les contacts men fichier

# ════════════════════════════════════════════════════
# ZONE HAUT : Titre
# ════════════════════════════════════════════════════
frame_haut = tk.Frame(root, bg="#4a90d9", pady=10)   # créer zone haut - couleur bleue
frame_haut.pack(fill="x")                             # pack fill="x" = katmtd f largeur kamla

tk.Label(
    frame_haut,                           # mettre le label f zone haut
    text="📒 Carnet d'Adresses",         # le texte li ghadi yban
    font=("Arial", 16, "bold"),           # police, taille, gras
    bg="#4a90d9",                         # couleur fond - nafs couleur dyal frame
    fg="white"                            # couleur texte - blanc
).pack()                                  # afficher le label

# ════════════════════════════════════════════════════
# ZONE MILIEU : Listbox (lista dyal les contacts)
# ════════════════════════════════════════════════════
frame_milieu = tk.Frame(root, pady=10)              # créer zone milieu
frame_milieu.pack(fill="both", expand=True, padx=10) # expand=True = takhed l'espace li bqa

listbox = tk.Listbox(
    frame_milieu,                         # mettre la listbox f zone milieu
    font=("Arial", 11),                   # police dyal les contacts
    selectbackground="#4a90d9",           # couleur selection - bleue
    height=12                             # 3dda dyal les lignes li katbanow
)
listbox.pack(fill="both", expand=True)    # afficher la listbox w tmtd f kol jiha

# ════════════════════════════════════════════════════
# FONCTION : afficher les contacts f la listbox
# ════════════════════════════════════════════════════
def afficher_contacts():
    listbox.delete(0, tk.END)             # hyed kol li kayn f listbox (bach n3awdo naffchow)
    contacts = carnet.get_all_contacts()  # jib les contacts men fichier
    contacts = sorted(contacts, key=lambda c: c.nom.lower())  # rتب alphabétiquement
    if not contacts:                      # ila ma kaynch contacts
        listbox.insert(tk.END, "Aucun contact.")   # affich message vide
    else:
        for c in contacts:                # dir boucle 3la kol contact
            listbox.insert(tk.END, f"{c.nom} | {c.email} | {c.telephone}")  # affich f listbox

afficher_contacts()                       # appel la fonction dab - bach tban les contacts men l'début

# ════════════════════════════════════════════════════
# FONCTION : ajouter un contact (popup)
# ════════════════════════════════════════════════════
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

    tk.Button(popup, text="✅ Confirmer", command=confirmer).pack(pady=15)  # ← manquait!
# ════════════════════════════════════════════════════
# FONCTION : supprimer le contact sélectionné
# ════════════════════════════════════════════════════
def supprimer():
    selection = listbox.curselection()    # jib l'index dyal contact li selectionniti
    if not selection:                     # ila ma selectinnich walo
        messagebox.showwarning("Attention", "Sélectionnez un contact à supprimer.")  # popup warning
        return                            # khroj men la fonction
    ligne = listbox.get(selection[0])    # jib le texte dyal la ligne selectionnée
    nom = ligne.split("|")[0].strip()    # khod ghir le nom (qbel | luwla)
    reponse = messagebox.askyesno("Confirmation", f"Supprimer '{nom}' ?")  # confirmation oui/non
    if reponse:                           # ila gal oui
        carnet.supprimer_contact(nom)     # supprimer men fichier
        afficher_contacts()               # refresh la listbox

# ════════════════════════════════════════════════════
# ZONE BAS : Boutons
# ════════════════════════════════════════════════════
frame_bas = tk.Frame(root, pady=10)       # créer zone bas
frame_bas.pack(fill="x", padx=10)        # afficher zone bas

tk.Button(
    frame_bas,                            # mettre le bouton f zone bas
    text="➕ Ajouter",                   # texte dyal bouton
    width=14,                             # 3rad dyal bouton
    command=fenetre_ajouter               # la fonction li tatkhdem mnin tclick
).pack(side="left", padx=5)              # side="left" = jib mn l'ysar

tk.Button(
    frame_bas,
    text="🗑 Supprimer",
    width=14,
    command=supprimer                     # relier au fonction supprimer
).pack(side="left", padx=5)

tk.Button(
    frame_bas,
    text="🔄 Actualiser",
    width=14,
    command=afficher_contacts             # relier au fonction afficher_contacts
).pack(side="left", padx=5)

# ── Lancer la fenêtre (dima f la fin !) ──────────────
root.mainloop()                           # lancer la boucle principale - ka-bqa la fenêtre mftoha
import tkinter as tk
from tkinter import messagebox
from authentification import verifier_admin


def lancer_login(callback_succes):
    # créer la fenêtre login
    fenetre_login = tk.Tk()
    fenetre_login.title("Connexion Admin")
    fenetre_login.geometry("300x200")

    # titre
    tk.Label(fenetre_login,
             text="Connexion Administrateur",
             font=("Arial", 12, "bold")).pack(pady=15)

    # champ username
    frame_user = tk.Frame(fenetre_login)
    frame_user.pack(pady=5)
    tk.Label(frame_user, text="Utilisateur :").pack(side="left")
    entry_user = tk.Entry(frame_user, width=20)
    entry_user.pack(side="left")

    # champ mot de passe (show="*" = masquer le texte)
    frame_mdp = tk.Frame(fenetre_login)
    frame_mdp.pack(pady=5)
    tk.Label(frame_mdp, text="Mot de passe :").pack(side="left")
    entry_mdp = tk.Entry(frame_mdp, width=20, show="*")
    entry_mdp.pack(side="left")

    def connecter():
        username = entry_user.get().strip()
        mot_de_passe = entry_mdp.get().strip()

        if verifier_admin(username, mot_de_passe):
            # si correct → fermer login et ouvrir l'application
            messagebox.showinfo("Succès", f"Bienvenue {username} !")
            fenetre_login.destroy()
            callback_succes()
        else:
            # si incorrect → message d'erreur
            messagebox.showerror("Erreur", "Identifiants incorrects !")
            entry_mdp.delete(0, tk.END)  # vider le champ mot de passe

    tk.Button(fenetre_login,
              text="Se connecter",
              command=connecter).pack(pady=15)

    fenetre_login.mainloop()
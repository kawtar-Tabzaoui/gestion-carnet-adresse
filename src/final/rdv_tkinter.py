import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from rdv import initialiser_rdv, get_creneaux, reserver_rdv, get_rdv_par_date, annuler_rdv

initialiser_rdv()

def lancer_rdv():
    root = tk.Tk()
    root.title("📅 Gestion des RDV")
    root.geometry("750x650")
    root.configure(bg="#f0f0f0")

    # ════════════════════════════════
    # TITRE
    # ════════════════════════════════
    tk.Label(root, text="📅 Gestion des RDV",
             font=("Arial", 16, "bold"),
             bg="#f0f0f0").pack(pady=10)

    # ════════════════════════════════
    # FRAME PRINCIPAL
    # ════════════════════════════════
    frame_main = tk.Frame(root, bg="#f0f0f0")
    frame_main.pack(fill="both", expand=True, padx=20)

    # ════════════════════════════════
    # CALENDRIER (gauche)
    # ════════════════════════════════
    frame_cal = tk.Frame(frame_main, bg="#f0f0f0")
    frame_cal.pack(side="left", padx=10)

    tk.Label(frame_cal, text="📆 Choisir une date",
             font=("Arial", 11, "bold"),
             bg="#f0f0f0").pack(pady=5)

    cal = Calendar(frame_cal,
                   selectmode="day",
                   date_pattern="yyyy-mm-dd",
                   font=("Arial", 10))
    cal.pack()

    # ════════════════════════════════
    # CRENEAUX (droite)
    # ════════════════════════════════
    frame_creneaux = tk.Frame(frame_main, bg="#f0f0f0")
    frame_creneaux.pack(side="left", padx=20, fill="both", expand=True)

    tk.Label(frame_creneaux, text="⏰ Créneaux disponibles",
             font=("Arial", 11, "bold"),
             bg="#f0f0f0").pack(pady=5)

    frame_scroll = tk.Frame(frame_creneaux)
    frame_scroll.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_scroll)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame_scroll,
                         font=("Arial", 11),
                         width=35,
                         yscrollcommand=scrollbar.set,
                         selectbackground="#4CAF50")
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    # ════════════════════════════════
    # CHAMPS NOM + MOTIF
    # ════════════════════════════════
    frame_info = tk.Frame(root, bg="#f0f0f0")
    frame_info.pack(pady=10)

    # Nom patient
    tk.Label(frame_info, text="👤 Nom du patient :",
             bg="#f0f0f0",
             font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
    entry_nom = tk.Entry(frame_info, width=20, font=("Arial", 11))
    entry_nom.grid(row=0, column=1, padx=5, pady=5)

    # Motif
    tk.Label(frame_info, text="📋 Motif du RDV :",
             bg="#f0f0f0",
             font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)

    motif_var = tk.StringVar(value="Consultation")
    motif_menu = tk.OptionMenu(frame_info, motif_var,
                               "Consultation",
                               "Urgence",
                               "Suivi",
                               "Contrôle",
                               "Autre")
    motif_menu.config(font=("Arial", 11), width=15)
    motif_menu.grid(row=1, column=1, padx=5, pady=5)

    # ════════════════════════════════
    # FONCTION : afficher créneaux
    # ════════════════════════════════
    def afficher_creneaux():
        listbox.delete(0, tk.END)
        date = cal.get_date()
        creneaux = get_creneaux(date)
        rdvs_reserves = get_rdv_par_date(date)
        heures_reservees = {r[0]: (r[1], r[2]) for r in rdvs_reserves}

        for heure in creneaux:
            if heure in heures_reservees:
                nom = heures_reservees[heure][0]
                motif = heures_reservees[heure][1]
                listbox.insert(tk.END, f"❌ {heure} — {nom} ({motif})")
                listbox.itemconfig(tk.END, fg="red")
            else:
                listbox.insert(tk.END, f"✅ {heure} — Libre")
                listbox.itemconfig(tk.END, fg="green")

    # ════════════════════════════════
    # FONCTION : réserver
    # ════════════════════════════════
    def reserver():
        date = cal.get_date()
        nom = entry_nom.get().strip()
        motif = motif_var.get()
        selection = listbox.curselection()

        if not nom:
            messagebox.showwarning("Attention", "Entrez le nom du patient !")
            return
        if not selection:
            messagebox.showwarning("Attention", "Choisissez un créneau !")
            return

        ligne = listbox.get(selection[0])
        if "réservé" in ligne or "❌" in ligne:
            messagebox.showerror("Erreur", "Ce créneau est déjà réservé !")
            return

        heure = ligne.split("—")[0].replace("✅", "").replace("❌", "").strip()
        result = reserver_rdv(date, heure, nom, motif)
        if result:
            messagebox.showinfo("Succès",
                f"✅ RDV réservé !\n\nDate: {date}\nHeure: {heure}\nPatient: {nom}\nMotif: {motif}")
            entry_nom.delete(0, tk.END)
            afficher_creneaux()
        else:
            messagebox.showerror("Erreur", "Créneau déjà réservé !")

    # ════════════════════════════════
    # FONCTION : annuler
    # ════════════════════════════════
    def annuler():
        date = cal.get_date()
        selection = listbox.curselection()

        if not selection:
            messagebox.showwarning("Attention", "Choisissez un créneau !")
            return

        ligne = listbox.get(selection[0])
        if "Libre" in ligne:
            messagebox.showwarning("Attention", "Ce créneau est déjà libre !")
            return

        heure = ligne.split("—")[0].replace("✅", "").replace("❌", "").strip()
        reponse = messagebox.askyesno("Confirmation",
                                       f"Annuler le RDV de {heure} ?")
        if reponse:
            annuler_rdv(date, heure)
            afficher_creneaux()
            messagebox.showinfo("Succès", "✅ RDV annulé !")

    # ════════════════════════════════
    # BOUTONS
    # ════════════════════════════════
    frame_boutons = tk.Frame(root, bg="#f0f0f0")
    frame_boutons.pack(pady=10)

    tk.Button(frame_boutons, text="📆 Afficher créneaux",
              width=18, bg="#2196F3", fg="white",
              font=("Arial", 11),
              command=afficher_creneaux).pack(side="left", padx=5)

    tk.Button(frame_boutons, text="✅ Réserver",
              width=12, bg="#4CAF50", fg="white",
              font=("Arial", 11),
              command=reserver).pack(side="left", padx=5)

    tk.Button(frame_boutons, text="❌ Annuler RDV",
              width=12, bg="#f44336", fg="white",
              font=("Arial", 11),
              command=annuler).pack(side="left", padx=5)

    # afficher créneaux au démarrage
    afficher_creneaux()

    root.mainloop()

lancer_rdv()
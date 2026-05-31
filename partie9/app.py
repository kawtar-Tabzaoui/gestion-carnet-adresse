from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import initialiser_bd, ajouter_contact, supprimer_contact, get_all_contacts, modifier_contact, verifier_admin, exporter_csv
from contact import Contact
import functools
from envoyer_email import envoyer_email as send_email
from whatsapp import generer_lien_whatsapp

app = Flask(__name__)
app.secret_key = "carnet123"

initialiser_bd()

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        mot_de_passe = request.form["mot_de_passe"]
        if verifier_admin(username, mot_de_passe):
            session["logged_in"] = True
            session["username"] = username
            flash("Bienvenue " + username + " !", "success")
            return redirect(url_for("index"))
        else:
            flash("Identifiants incorrects !", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    contacts = get_all_contacts()
    return render_template("index.html", contacts=contacts)

@app.route("/ajouter", methods=["GET", "POST"])
@login_required
def ajouter():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        categorie = request.form["categorie"]
        adresse = request.form["adresse"]
        fonction = request.form["fonction"]
        entreprise = request.form["entreprise"]
        try:
            Contact(nom, email, telephone)
            result, doublon = ajouter_contact(
                nom,
                email,
                telephone,
                categorie,
                adresse,
                fonction,
                entreprise
            )
            if result:
                flash("Contact ajouté avec succès !", "success")
            else:
                flash(f"Le {doublon} existe déjà !", "error")
        except AssertionError as e:
            flash(str(e), "error")
        return redirect(url_for("index"))
    return render_template("ajouter.html")

@app.route("/supprimer", methods=["GET", "POST"])
@login_required
def supprimer():
    if request.method == "POST":
        info = request.form["info"]
        result = supprimer_contact(info)
        if result:
            flash("Contact supprimé !", "success")
        else:
            flash("Contact non trouvé !", "error")
        return redirect(url_for("index"))
    return render_template("supprimer.html")

@app.route("/supprimer_direct/<int:id>")
@login_required
def supprimer_direct(id):
    supprimer_contact(str(id))
    flash("Contact supprimé !", "success")
    return redirect(url_for("index"))

@app.route("/envoyer_email/<int:id>", methods=["GET", "POST"])
@login_required
def envoyer_email(id):
    contacts = get_all_contacts()
    contact = next((c for c in contacts if c[0] == id), None)
    if request.method == "POST":
        destinataire = request.form["destinataire"]
        sujet = request.form["sujet"]
        message = request.form["message"]
        result, msg = send_email(destinataire, sujet, message)
        flash(msg, "success" if result else "error")
        return redirect(url_for("index"))
    return render_template("email.html", contact=contact)



@app.route("/whatsapp/<int:id>", methods=["GET", "POST"])
@login_required
def whatsapp(id):
    contacts = get_all_contacts()
    contact = next((c for c in contacts if c[0] == id), None)
    if request.method == "POST":
        message = request.form["message"]
        lien = generer_lien_whatsapp(contact[3], message)
        flash("Message WhatsApp prêt ✅ !", "success")
        return redirect(lien)
    return render_template("whatsapp.html", contact=contact)

@app.route("/modifier/<int:id>", methods=["GET", "POST"])
@login_required
def modifier(id):
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        categorie = request.form["categorie"]
        adresse = request.form["adresse"]
        fonction = request.form["fonction"]
        entreprise = request.form["entreprise"]
        try:
            Contact(nom, email, telephone)
            modifier_contact(
                id,
                nom,
                email,
                telephone,
                categorie,
                adresse,
                fonction,
                entreprise
            )
            flash("Contact modifié !", "success")
        except AssertionError as e:
            flash(str(e), "error")
        return redirect(url_for("index"))
    contacts = get_all_contacts()
    contact = next((c for c in contacts if c[0] == id), None)
    return render_template("modifier.html", contact=contact)

@app.route("/exporter")
@login_required
def exporter():
    exporter_csv()
    flash("Contacts exportés dans contacts_export.csv !", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
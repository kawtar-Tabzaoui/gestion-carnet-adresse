import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL = "kawtartabzaoui@gmail.com"
APP_PASSWORD = "kbcz vcnr rsls ohwc"

def envoyer_email(destinataire, sujet, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL
        msg["To"] = destinataire
        msg["Subject"] = sujet
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL, APP_PASSWORD)
        server.sendmail(GMAIL, destinataire, msg.as_string())
        server.quit()

        return True, "Email envoyé avec succès ✅"
    except Exception as e:
        return False, f"Erreur : {str(e)}"
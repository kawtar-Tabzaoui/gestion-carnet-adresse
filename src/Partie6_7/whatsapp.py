def generer_lien_whatsapp(telephone, message):
    numero = "212" + telephone[1:]
    import urllib.parse
    message_encode = urllib.parse.quote(message)
    lien = f"https://wa.me/{numero}?text={message_encode}"
    return lien
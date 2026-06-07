import re
class Contact:
    def __init__(self,nom,email,telephone):
        assert isinstance(nom,str) and len(nom)>0, "le nom non valide"

        assert isinstance(email,str) and len(email)>0, "email non valide"
        emai_structure = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        assert re.match(emai_structure,email),"email non valide"

        assert telephone.isdigit() and len(telephone) == 10, "Téléphone doit contenir 10 chiffres"
        assert telephone.startswith("06") or telephone.startswith("07"), "Téléphone doit commencer par 06 ou 07"
        self.nom = nom
        self.email = email
        self.telephone = telephone
    def __str__(self):
        return f"Nom: {self.nom} | Email: {self.email} | Telephone: {self.telephone}"

#contact1 = Contact("kawtar tabzaoui","kawtartabzaoui@gmail.com","0909090903")
#contact2 = Contact("wissal Faiz","wissalFaiz@","0909090903")
#print(contact1)
#print(contact2)



# /w



#if "@" not in email or "." not in email:
            #print("email not valide")
            #return

# valider la structure schene de caractere e, add sch une autre .autre chaine
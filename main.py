import datetime

class Enquete():

    id = 1
    enquetes = []

    def __init__(self, nom:str, date_de_debut:str, date_de_fin:str, listes_preuves=[], personne_impliquee=[]):
        self.id = Enquete.id
        Enquete.id += 1
        self.nom = nom
        self.date_de_debut = datetime.datetime.strptime(date_de_debut, '%Y-%m-%d').strftime('%d/%m/%Y')
        self.date_de_fin = datetime.datetime.strptime(date_de_fin, '%Y-%m-%d').strftime('%d/%m/%Y')
        self.listes_preuves = listes_preuves
        self.personne_impliquee = personne_impliquee
        Enquete.enquetes.append(self)

    def __str__(self):
        return f"{self.id} {self.nom} {self.date_de_debut} {self.date_de_fin} {self.listes_preuves} {self.personne_impliquee}"

    def add_dates_interrogatoires(self, enqueteur, repondant):
        return enqueteur, repondant

    def add_personne(self, personne):
        return self.personne_impliquee.append(personne)

    def get_enquetes_liees(self):
        return self.listes_preuves

    def add_evenement(self):
        return self.listes_preuves

    def cloturer_enquete(self):
        # Supprimer cette instance de la liste d'enquêtes
        Enquete.enquetes.remove(self)
        print(f"L'enquête '{self.nom}' a été clôturée et supprimée.")

    @classmethod
    def afficher_enquetes(cls):
        for enquete in cls.enquetes:
            print(enquete)

enquete1 = Enquete("Meurtre", "2003-08-04", "2005-02-26", [], [])
enquete2 = Enquete("Cambriolage", "2010-06-15", "2011-08-01", [], [])

# Affichage des enquêtes
print("Enquêtes avant clôture:")
Enquete.afficher_enquetes()

# Clôturer une enquête
enquete1.cloturer_enquete()

# Affichage des enquêtes après la clôture
print("\nEnquêtes après clôture:")
Enquete.afficher_enquetes()

from person import Person
import utils

class Enquete():

    id = 1
    enquetes = []

    def __init__(self, nom:str, date_de_debut:str, date_de_fin:str, listes_preuves=[], personne_impliquee=[]) -> None:
        self.id = Enquete.id
        Enquete.id += 1
        self.nom = nom
        self.date_de_debut = utils.convertir_date(date_de_debut)
        self.date_de_fin = utils.convertir_date(date_de_fin)
        self.listes_preuves = listes_preuves
        self.personne_impliquee = personne_impliquee
        Enquete.enquetes.append(self)

    def __str__(self) -> str:
        # Utilisation de `str(personne)` pour chaque personne dans `personne_impliquee`
        personnes = ', '.join(str(personne) for personne in self.personne_impliquee)
        return (f"Rapport de l'enquête n°{self.id} concernant un/une {self.nom}, \n"
                f"Enquête ID: {self.id}, Titre: {self.nom}, \n"
                f"Début: {self.date_de_debut}, Fin: {self.date_de_fin}, \n"
                f"Preuves: {self.listes_preuves}, \nPersonnes impliquées: {personnes}\n")

    def afficher_dates_interrogatoires(self, enqueteur, repondant):
        return enqueteur, repondant

    def add_personne(self, nomPers, prenPers, dateNaissance):
        return self.personne_impliquee.append(Person(nomPers, prenPers, dateNaissance))

    def get_enquetes_liees(self):
        return self.listes_preuves

    def add_evenement(self):
        return self.listes_preuves
    
    def generer_rapport(self, id):
        for enquete in Enquete.enquetes:
            if enquete.id == id:
                print(enquete)  # Utilise `__str__` pour afficher l'enquête
                return
        # Si aucune enquête avec cet ID n'est trouvée
        print(f"Aucune enquête trouvée avec l'ID {id}.")

    def cloturer_enquete(self) -> None:
        # Supprimer cette instance de la liste d'enquêtes
        Enquete.enquetes.remove(self)
        print(f"L'enquête '{self.nom}' a été clôturée et supprimée.\n")

enquete1 = Enquete("Meurtre", "2003-08-04", "2005-02-26", [], [])
enquete2 = Enquete("Cambriolage", "2010-06-15", "2011-08-01", [], [])
enquete1.add_personne("David", "Bowie", "1990-06-12")
enquete2.add_personne("Marie", "Curie", "1902-11-26")

# Clôturer une enquête
#enquete2.cloturer_enquete()

#Générer un rapport
enquete1.generer_rapport(1)
enquete1.generer_rapport(2)

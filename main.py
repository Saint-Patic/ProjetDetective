from classes.event import Evenement
from classes.person import Person
# from classes.criminel import Criminel
# from classes.temoin import Temoin
# from classes.suspect import Suspect
# from classes.employe import Employe
import utils

class Enquete:

    id = 1
    enquetes = []

    def __init__(self, nom:str, date_de_debut:str, date_de_fin:str, liste_preuves=[], personne_impliquee=[]) -> None:
        self.id = Enquete.id
        Enquete.id += 1
        self.nom = nom
        self.date_de_debut = utils.convertir_date(date_de_debut)
        self.date_de_fin = utils.convertir_date(date_de_fin)
        self.liste_preuves = liste_preuves
        self.personne_impliquee = personne_impliquee
        self.liste_evenement = []
        Enquete.enquetes.append(self)

    def __str__(self) -> str:
        # Utilisation de `str(personne)` pour chaque personne dans `personne_impliquee`
        personnes = ', '.join(str(personne) for personne in self.personne_impliquee)
        return (f"Rapport de l'enquête n°{self.id} concernant un/une {self.nom}, \n"
                f"Enquête ID: {self.id}, Titre: {self.nom}, \n"
                f"Début: {self.date_de_debut}, Fin: {self.date_de_fin}, \n"
                f"Preuves: {self.liste_preuves}, \nPersonnes impliquées: {personnes}\n")

    def afficher_interrogatoires(self, num_enquete):
        interrogatoires_trouves = False  # Indicateur pour vérifier si des interrogatoires ont été trouvés

        for personne in self.personne_impliquee:
            # Vérifier si l'objet `personne` a l'attribut `interrogatoires` et qu'il n'est pas vide
            if hasattr(personne, 'interrogatoires') and personne.interrogatoires:
                interrogatoires_personne = [
                    (date, interrogatoire)  # Conserver la date en même temps que l'interrogatoire
                    for date, interrogatoires in personne.interrogatoires.items()
                    for interrogatoire in interrogatoires if interrogatoire['num_enquete'] == num_enquete
                ]

                if interrogatoires_personne:
                    print(f"Interrogatoires pour {personne.nom} {personne.prenom}:")
                    for date, interrogatoire in interrogatoires_personne:  # Utilisation de `date` ici
                        print(f"  Date: {date}")
                        print(f"  Enquêteur: {interrogatoire['enqueteur']}")
                        print(f"  Numéro d'enquête: {interrogatoire['num_enquete']}")
                        interrogatoires_trouves = True
            else:
                print(f"{personne.nom} {personne.prenom} n'a pas d'interrogatoires.")

        if not interrogatoires_trouves:
            print(f"Aucun interrogatoire trouvé pour l'enquête ID {num_enquete}.")

    def add_personne(self, personne):
        return self.personne_impliquee.append(personne)

    def get_enquetes_liees(self):
        return self.enquetes

    def add_evenement(self, nom_evenement):
        return self.liste_evenement.append(Evenement(nom_evenement, self.id))
    
    def generer_rapport(self, id):
        for enquete in Enquete.enquetes:
            if enquete.id == id:
                print(enquete)  
                return
        # Si aucune enquête avec cet ID n'est trouvée
        print(f"Aucune enquête trouvée avec l'ID {id}.")

    def cloturer_enquete(self) -> None:
        # Supprimer cette instance de la liste d'enquêtes
        Enquete.enquetes.remove(self)
        print(f"L'enquête '{self.nom}' a été clôturée et supprimée.\n")

    def afficher_enquetes():
        for enquete in Enquete.enquetes:
            print(enquete)


if __name__ == "__main__":

    Meurtre = Enquete("Meurtre", "2003-08-04", "2005-02-26", [], [])
    Cambriolage = Enquete("Cambriolage", "2010-06-15", "2011-08-01", [], [])
    Alexis = Person("Demarcq", "Alexis", "2003-08-04", "Homme")
    Nathan = Person("Lemaire", "Nathan", "2003-01-01", "Homme")
    Quentin = Person("Henrard", "Quentin", "2003-08-04", "Homme")

    Meurtre.add_personne(Alexis)
    Meurtre.add_personne(Quentin)
    Cambriolage.add_personne(Alexis)
    Cambriolage.add_personne(Quentin)

    Alexis.add_interrogatoire("2004-01-01", Nathan, Meurtre.id)
    Quentin.add_interrogatoire("2005-11-22", Nathan, Cambriolage.id)
    Alexis.add_interrogatoire("2004-01-21", Nathan, Cambriolage.id)

    Enquete.afficher_enquetes()

    # # Afficher les évènements
    # print(Meurtre.liste_evenement)
    # Meurtre.add_evenement("Découverte du corps")
    # print(Meurtre.liste_evenement[0])

    # # Afficher les interrogatoires
    # Meurtre.afficher_interrogatoires(Meurtre.id)
    # Cambriolage.afficher_interrogatoires(Cambriolage.id)

    # # Clôturer une enquête
    # enquete2.cloturer_enquete()

    # #Générer un rapport
    # Meurtre.generer_rapport(1)
    # Cambriolage.generer_rapport(2)

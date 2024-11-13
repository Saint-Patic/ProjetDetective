from classes.preuves import Preuve
from classes.event import Evenement
from classes.person import Person
import utils


class Enquete:
    id = 1
    enquetes = []

    def __init__(self, nom: str, date_de_debut: str, date_de_fin: str, liste_preuves=[], personne_impliquee=[]) -> None:
        self.id = Enquete.id
        Enquete.id += 1
        self.nom = nom
        self.date_de_debut = utils.convertir_date(date_de_debut)
        self.date_de_fin = utils.convertir_date(date_de_fin)
        self.liste_preuves: list = liste_preuves
        self.personne_impliquee = personne_impliquee
        self.liste_evenement = []
        self.id_preuve = 0
        self.enquetes_liees: list = []
        Enquete.enquetes.append(self)

    def __str__(self) -> str:
        if len(self.liste_preuves) == 0:
            preuves = "Aucune preuves dans cette enquête."
        else:
            preuves = ', '.join(str(preuve) for preuve in self.liste_preuves)
        if self.personne_impliquee == []:
            personnes = "Aucune personnes impliquées dans cette enquête."
        else:
            personnes = ', '.join(str(personne) for personne in self.personne_impliquee)

        return (f"Rapport de l'enquête n°{self.id} concernant un/une {self.nom} \n"
                f"Enquête ID: {self.id} Titre: {self.nom} \n"
                f"Début: {self.date_de_debut} Fin: {self.date_de_fin} \n"
                f"Preuves: {preuves} \nPersonnes impliquées: {personnes}\n")

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
                        print(f"  Numéro d'enquête: {interrogatoire['num_enquete']}\n")
                        interrogatoires_trouves = True
            else:
                print(f"{personne.nom} {personne.prenom} n'a pas d'interrogatoires.")

        if not interrogatoires_trouves:
            print(f"Aucun interrogatoire trouvé pour l'enquête ID {num_enquete}.")

    def add_personne(self, personne):
        return self.personne_impliquee.append(personne)

    def add_enquetes_liees(self, enquete):
        return self.enquetes_liees.append(enquete)

    def afficher_enquetes_liees(self):
        if self.enquetes_liees == []:
            return print(f"Aucune enquête liée à l'enquête {self.nom}.\n")
        print(f"Enquêtes liées pour l'enquête {self.nom}:\n")
        for i in self.enquetes_liees:
            print(i)

    def add_evenement(self, nom_evenement):
        return self.liste_evenement.append(Evenement(nom_evenement, self.id))

    def afficher_evenements(self):
        if self.liste_evenement == []:
            return print(f"Aucun évènements trouvés pour l'enquête {self.nom}.\n")
        print(f"Evènements pour l'enquête {self.nom}:\n")
        for evenement in self.liste_evenement:
            print(evenement)

    def add_preuves(self, nom_preuves):
        self.id_preuve += 1
        return self.liste_preuves.append(Preuve(self.id_preuve, nom_preuves, self.id))

    def afficher_preuves(self):
        if self.liste_preuves == []:
            return print(f"Aucune preuves trouvées pour l'enquête {self.nom}.\n")
        print(f"Preuves pour l'enquête {self.nom}:\n")
        for preuve in self.liste_preuves:
            print(preuve)

    def generer_rapport(id):
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

    # # Afficher les enquêtes liées
    # Meurtre.afficher_enquetes_liees()
    # Meurtre.add_enquetes_liees(Cambriolage)
    # Meurtre.afficher_enquetes_liees()

    # # Afficher les preuves
    # Meurtre.add_preuves("Arme")
    # Meurtre.add_preuves("Indice")
    # Cambriolage.add_preuves("Arme")
    # Meurtre.afficher_preuves()
    # Cambriolage.afficher_preuves()

    # # Afficher les enquêtes existantes
    # Enquete.afficher_enquetes()

    # # Afficher les évènements
    # Meurtre.add_evenement("Découverte du corps")
    # Meurtre.afficher_evenements()
    # Cambriolage.afficher_evenements()

    # # Afficher les interrogatoires
    # Alexis.add_interrogatoire("2004-01-01", Nathan, Meurtre.id)
    # Quentin.add_interrogatoire("2005-11-22", Nathan, Cambriolage.id)
    # Alexis.add_interrogatoire("2002-01-21", Nathan, Cambriolage.id)
    # Meurtre.afficher_interrogatoires(Meurtre.id)
    # Cambriolage.afficher_interrogatoires(Cambriolage.id)

    # # Clôturer une enquête
    # Cambriolage.cloturer_enquete()

    # # Générer un rapport
    # Enquete.generer_rapport(1)
    # Enquete.generer_rapport(2)

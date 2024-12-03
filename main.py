from classes import Personne, Temoin, Suspect, Employe, Criminel, Evenement, Preuve
from datetime import datetime
import utils
import json


class Enquete:

    id = 1
    enquetes = []

    def __init__(
        self,
        nom: str,
        date_de_debut: str,
        date_de_fin="Enquête non clôturer",
        liste_preuves=[],
        personne_impliquee=[],
    ) -> None:
        self.id = Enquete.id
        Enquete.id += 1
        self.nom = nom
        self.date_de_debut = utils.convertir_date(date_de_debut)
        self.date_de_fin = utils.convertir_date(date_de_fin)
        self.liste_preuves = liste_preuves
        self.personne_impliquee = personne_impliquee
        self.liste_evenement = []
        self.id_preuve = 0
        self.enquetes_liees = []
        Enquete.enquetes.append(self)
        self.id_event = 0

    def __str__(self) -> str:
        if self.liste_preuves == []:
            preuves = "Aucune preuves dans cette enquête."
        else:
            preuves = ", ".join(str(preuve) for preuve in self.liste_preuves)
        if self.personne_impliquee == []:
            personnes = "Aucune personnes impliquées dans cette enquête."
        else:
            personnes = ", ".join(str(personne) for personne in self.personne_impliquee)

        return (
            f"Rapport de l'enquête n°{self.id} concernant un/une {self.nom} \n"
            f"Enquête ID: {self.id} Titre: {self.nom} \n"
            f"Début: {self.date_de_debut} Fin: {self.date_de_fin} \n"
            f"Preuves: {preuves} \nPersonnes impliquées: {personnes}\n"
        )

    def afficher_interrogatoires(self, num_enquete):
        interrogatoires_trouves = (
            False  # Indicateur pour vérifier si des interrogatoires ont été trouvés
        )

        for personne in self.personne_impliquee:
            # Vérifier si l'objet `personne` a l'attribut `interrogatoires` et qu'il n'est pas vide
            if hasattr(personne, "interrogatoires") and personne.interrogatoires:
                interrogatoires_personne = [
                    (
                        date,
                        interrogatoire,
                    )  # Conserver la date en même temps que l'interrogatoire
                    for date, interrogatoires in personne.interrogatoires.items()
                    for interrogatoire in interrogatoires
                    if interrogatoire["num_enquete"] == num_enquete
                ]

                if interrogatoires_personne:
                    print(f"Interrogatoires pour {personne.nom} {personne.prenom}:")
                    for (
                        date,
                        interrogatoire,
                    ) in interrogatoires_personne:  # Utilisation de `date` ici
                        print(f"  Date: {date}")
                        print(f"  Enquêteur: {interrogatoire['enqueteur']}")
                        print(f"  Numéro d'enquête: {interrogatoire['num_enquete']}")
                        interrogatoires_trouves = True

            else:
                print(f"{personne.nom} {personne.prenom} n'a pas d'interrogatoires.")

        if not interrogatoires_trouves:
            print(f"Aucun interrogatoire trouvé pour l'enquête ID {num_enquete}.")

        print("\n")

    def add_personne(self, personne):
        try:
            with open("fichiers/personnes.json", "r", encoding="utf-8") as json_file:
                donnees_existantes = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees_existantes = []

        # Convertir l'objet personne en dictionnaire complet
        dict_personne = {
            "nom": personne.nom,
            "prenom": personne.prenom,
            "classe": personne.__class__.__name__,
            "sexe": personne.sexe,
            "date_de_naissance": personne.date_de_naissance,
            "metier": getattr(personne, "metier", ""),
            "mail": getattr(personne, "mail", ""),
            "interrogatoires": getattr(personne, "interrogatoires"),
        }

        # Ajouter les attributs supplémentaires si disponibles
        for attr, valeur in personne.__dict__.items():
            if attr not in [
                "nom",
                "prenom",
                "sexe",
                "_date_de_naissance",
                "_date_de_deces",
                "metier",
                "mail",
                "interrogatoires",
            ]:
                dict_personne[attr] = valeur

        # Chercher si la personne existe déjà dans les données
        for index, existing_personne in enumerate(donnees_existantes):
            if (
                existing_personne["nom"] == personne.nom
                and existing_personne["prenom"] == personne.prenom
                and existing_personne["date_de_naissance"] == personne.date_de_naissance
            ):
                # Mettre à jour les informations existantes avec les nouvelles valeurs
                donnees_existantes[index] = dict_personne
                break
        else:
            # Si la personne n'est pas trouvée, ajouter comme nouvelle
            donnees_existantes.append(dict_personne)

        # Sauvegarder les données mises à jour dans le fichier
        with open("fichiers/personnes.json", "w", encoding="utf-8") as json_file:
            json.dump(donnees_existantes, json_file, indent=4, ensure_ascii=False)

        # Ajouter la personne à la liste des personnes impliquées
        self.personne_impliquee.append(personne)

    def sauvegarder_enquete(self):
        try:
            with open("fichiers/enquetes.json", "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = []
        enquete_dict = self.to_dict()

        for index, enquete in enumerate(donnees):
            if enquete["id"] == self.id:
                donnees[index] = enquete_dict
                break
        else:
            donnees.append(enquete_dict)

        with open("fichiers/enquetes.json", "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, indent=4, ensure_ascii=False)

    def add_enquetes_liees(self, enquete):
        """Ajoute une enquête liée et met à jour le fichier enquetes.json."""
        if enquete not in self.enquetes_liees:
            self.enquetes_liees.append(enquete)
            self.sauvegarder_enquete()

    def afficher_enquetes_liees(self, indentation=4):
        if not self.enquetes_liees:
            print(f"Aucune enquête liée à l'enquête {self.nom}.\n")
            return

        print(f"Enquêtes liées pour l'enquête {self.nom}:")
        for enquete in self.enquetes_liees:
            enquete_str = str(enquete)
            print(utils.ajouter_indentation(enquete_str, indentation))

        print("\n")

    def add_evenement(self, nom_evenement):
        self.id_event += 1
        nouvel_evenement = Evenement(self.id_event, nom_evenement, self.id)
        try:
            with open("fichiers/evenement.json", "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = []
        evenement_dict = nouvel_evenement.to_dict()

        for index, evenement in enumerate(donnees):
            if evenement["id"] == self.id_event:
                donnees[index] = evenement_dict
                break
        else:
            donnees.append(evenement_dict)

        with open("fichiers/evenement.json", "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, indent=4, ensure_ascii=False)
        self.liste_evenement.append(nouvel_evenement)

    def afficher_evenements(self, indentation=4):
        if self.liste_evenement == []:
            return print(f"Aucun évènements trouvés pour l'enquête {self.nom}.\n")
        print(f"Evènements pour l'enquête {self.nom}:")
        for evenement in self.liste_evenement:
            evenement_str = str(evenement)
            print(utils.ajouter_indentation(evenement_str, indentation))

        print("\n")

    def add_preuves(self, nom_preuves):
        self.id_preuve += 1
        return self.liste_preuves.append(Preuve(self.id_preuve, nom_preuves, self.id))

    def afficher_preuves(self, indentation=4):
        if self.liste_preuves == []:
            return print(f"Aucune preuves trouvées pour l'enquête {self.nom}.\n")
        print(f"Preuves pour l'enquête {self.nom}:")
        for preuve in self.liste_preuves:
            preuve_str = str(preuve)
            print(utils.ajouter_indentation(preuve_str, indentation))

        print("\n")

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

    def to_dict(self):
        if isinstance(self.date_de_debut, str):
            self.date_de_debut = utils.convertir_date(self.date_de_debut)
        if isinstance(self.date_de_fin, str):
            self.date_de_fin = utils.convertir_date(self.date_de_fin)
        return {
            "id": self.id,
            "nom": self.nom,
            "date_de_debut": utils.convertir_date(self.date_de_debut),
            "date_de_fin": utils.convertir_date(self.date_de_fin),
            "liste_preuves": [preuve.to_dict() for preuve in self.liste_preuves],
            "personne_impliquee": [
                personne.to_dict() for personne in self.personne_impliquee
            ],
            "liste_evenement": [
                evenement.to_dict() for evenement in self.liste_evenement
            ],
            "enquetes_liees": [e.id for e in self.enquetes_liees],
        }


def creer_enquete(nom, date_de_debut, date_de_fin):
    """Crée une nouvelle enquête et la sauvegarde dans enquetes.json."""
    try:
        utils.convertir_date(date_de_debut)
        utils.convertir_date(date_de_fin)
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYY-MM-DD.")

    nouvelle_enquete = Enquete(nom, date_de_debut, date_de_fin)
    return nouvelle_enquete


if __name__ == "__main__":

    Vol = creer_enquete("Vol", "2023-01-01", "2023-06-30")
    Fraude = creer_enquete("Fraude", "2023-07-01", "2023-12-31")
    Meurtre = Enquete("Meurtre", "2003-08-04", "2005-02-26", [], [])
    Cambriolage = Enquete("Cambriolage", "2010-06-15", "2011-08-01", [], [])

    Alexis = Personne("Demarcq", "Alexis", "2003-08-04", "Homme")
    Nathan = Employe("Lemaire", "Nathan", "2003-01-01", "Homme")
    Quentin = Suspect("Henrard", "Quentin", "2003-08-04", "Homme")
    Tristan = Criminel("Valcke", "Tristan", "2003-08-04", "Homme")

    Meurtre.add_personne(Alexis)
    Meurtre.add_personne(Quentin)
    Cambriolage.add_personne(Alexis)
    Cambriolage.add_personne(Nathan)

    # Afficher les enquêtes liées
    Vol.add_enquetes_liees(Fraude)
    Meurtre.afficher_enquetes_liees()
    Meurtre.add_enquetes_liees(Cambriolage)
    Meurtre.afficher_enquetes_liees()
    Vol.afficher_enquetes_liees()

    # Sauvegarder les enquêtes
    Vol.sauvegarder_enquete()
    Fraude.sauvegarder_enquete()
    Meurtre.sauvegarder_enquete()
    Cambriolage.sauvegarder_enquete()

    # # Afficher les preuves
    # Meurtre.add_preuves("Arme")
    # Meurtre.add_preuves("Indice")
    # Cambriolage.add_preuves("Arme")
    # Meurtre.afficher_preuves()
    # Cambriolage.afficher_preuves()

    # # Afficher les enquêtes existantes
    # Enquete.afficher_enquetes()

    # Afficher les évènements
    Meurtre.add_evenement("Découverte du corps")
    Meurtre.afficher_evenements()
    Cambriolage.afficher_evenements()

    # Afficher les interrogatoires
    Alexis.ajouter_interrogatoire("2004-01-01", Nathan, Meurtre.id)
    Quentin.ajouter_interrogatoire("2005-11-22", Nathan, Cambriolage.id)
    Alexis.ajouter_interrogatoire("2002-01-21", Nathan, Cambriolage.id)
    Meurtre.afficher_interrogatoires(Meurtre.id)
    Cambriolage.afficher_interrogatoires(Cambriolage.id)

    # # Clôturer une enquête
    # Cambriolage.cloturer_enquete()

    # # Générer un rapport
    # Enquete.generer_rapport(1)
    # Enquete.generer_rapport(2)

from utilitaire import utils
import json
import datetime
from classes import (
    Personne,
    Temoin,
    Suspect,
    Employe,
    Criminel,
    Evenement,
    Preuve,
    Enquete,
)
import GUI


def charger_donnees(chemin_fichier):
    """Charge les données JSON depuis un fichier."""
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def creer_enquete(nom, date_de_debut, date_de_fin):
    """Crée une nouvelle enquête et la sauvegarde dans enquetes.json."""
    try:
        utils.convertir_date(date_de_debut)
        utils.convertir_date(date_de_fin)
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYY-MM-DD.")

    if date_de_debut > date_de_fin:
        raise ValueError("La date de début doit être inférieure à la date de fin.")
    if date_de_debut > utils.convertir_date(datetime.datetime.now()):
        raise ValueError("La date de début ne peut pas être dans le futur.")

    nouvelle_enquete = Enquete(nom, date_de_debut, date_de_fin)
    nouvelle_enquete.sauvegarder_enquete()
    return nouvelle_enquete


def afficher_enquete():
    """Affiche les enquêtes existantes et retourne une liste d'enquêtes."""
    with open("fichiers/enquetes.json", "r", encoding="utf-8") as f:
        enquetes = json.load(f)
        for idx, enquete in enumerate(enquetes, 1):
            print(
                f"{idx}. {enquete['nom']} ({enquete['date_de_debut']} - {enquete['date_de_fin']})"
            )
    return enquetes


def choisir_enquete(enquetes):
    """Permet de choisir une enquête parmi celles listées."""

    try:
        num_enquete = int(input("Choisir un numéro d'enquête: "))
        if num_enquete < 1 or num_enquete > len(enquetes):
            print("Numéro invalide.")
            return None
        # Convertir l'enquête en une instance de la classe Enquete
        enquete_choisie = enquetes[num_enquete - 1]

        # Crée une instance de la classe Enquete avec toutes les informations
        enquête_instance = Enquete(
            enquete_choisie["nom"],
            utils.convertir_date(enquete_choisie["date_de_debut"]),
            utils.convertir_date(enquete_choisie["date_de_fin"]),
        )
        enquête_instance.personne_impliquee = enquete_choisie.get(
            "personne_impliquee", []
        )
        enquête_instance.liste_evenement = enquete_choisie.get("liste_evenement", [])
        enquête_instance.liste_preuves = enquete_choisie.get("liste_preuves", [])
        enquête_instance.enquetes_liees = enquete_choisie.get("enquetes_liees", [])
        enquête_instance.id_preuve = enquete_choisie.get("id", 0)

        return enquête_instance

    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return None


if __name__ == "__main__":
    sortie = False
    ajout = True
    nom_dossier = "fichiers/"
    evenement_brut = charger_donnees(f"{nom_dossier}evenement.json")
    interro_brut = charger_donnees(f"{nom_dossier}interrogatoires.json")
    enquete_brut = charger_donnees(f"{nom_dossier}enquetes.json")
    pers_brut = charger_donnees(f"{nom_dossier}personnes.json")
    preuve_brut = charger_donnees(f"{nom_dossier}preuves.json")
    while not sortie:
        print("\nMenu:")
        print("1. Créer une nouvelle enquête")
        print("2. Choisir une enquête")
        print("3. Afficher les enquêtes existantes")
        print("4. Quitter")
        choix = input("Votre choix: ")
        if choix == "1":
            nom = input("    Nom de l'enquête: ")
            date_de_debut = input("Date de début (YYYY-MM-DD): ")
            date_de_fin = input("Date de fin (YYYY-MM-DD): ")
            nouvelle_enquete = creer_enquete(nom, date_de_debut, date_de_fin)
            print(f"Enquête créée: {nouvelle_enquete}")
        elif choix == "2":
            enquetes = afficher_enquete()
            enquete_choisie = choisir_enquete(enquetes)
            if enquete_choisie:
                while ajout:
                    print("1. ajouter une personne ")
                    print("2. lier une enquete ")
                    print("3. ajouter un évènement ")
                    print("4. ajouter une preuve ")
                    print("5. retour menu")
                    choix_ajout = input("Votre choix: ")
                    if choix_ajout == "1":
                        enquete_choisie.afficher_personne()
                        print(
                            f"{len(enquete_choisie.personne_impliquee) + 1}. créer une nouvelle personne"
                        )
                        choix_personne = input(
                            f"Ajouter une personne déjà dans la base de donnée (1 - {len(enquete_choisie.personne_impliquee)} ou en ajouter une nouvelle {len(enquete_choisie.personne_impliquee) + 1} : "
                        )

                    elif choix_ajout == "2":
                        enquete_choisie.afficher_enquetes_liees()
                    elif choix_ajout == "3":
                        enquete_choisie.afficher_evenements()
                    elif choix_ajout == "4":
                        enquete_choisie.afficher_preuves()
                    elif choix_ajout == "5":
                        ajout = False

        elif choix == "3":
            GUI.PoliceManagementApp().run()
            break
        elif choix == "4":
            break

        rep = input("Quitter (oui/non) ? ")
        sortie = True if rep == "oui" else False

from utilitaire import utils
import json
import datetime
from colorama import Fore, Style, init
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
from utilitaire.commandes_terminale import *

init(autoreset=True)


if __name__ == "__main__":
    sortie = False
    nom_dossier = "fichiers/"
    evenement_brut = charger_donnees(f"{nom_dossier}evenement.json")
    interro_brut = charger_donnees(f"{nom_dossier}interrogatoires.json")
    enquete_brut = charger_donnees(f"{nom_dossier}enquetes.json")
    pers_brut = charger_donnees(f"{nom_dossier}personnes.json")
    preuve_brut = charger_donnees(f"{nom_dossier}preuves.json")

    while not sortie:
        print(Fore.CYAN + "\nMenu Principal:")
        print(Fore.YELLOW + "1. Gestion des enquêtes")
        print(Fore.YELLOW + "2. Consultation des données")
        print(Fore.YELLOW + "3. Interface graphique (lancer l'application)")
        print(Fore.YELLOW + "4. Quitter")

        choix = input(Fore.GREEN + f"{4 * ' '}Votre choix: ")

        if choix == "1":
            print(Fore.CYAN + "\nGestion des Enquêtes:")
            print(Fore.YELLOW + "1. Créer une nouvelle enquête")
            print(Fore.YELLOW + "2. Modifier une enquête existante")
            print(Fore.YELLOW + "3. Supprimer une enquête")
            print(Fore.YELLOW + "4. Retour au menu principal")

            choix_enquete = input(Fore.GREEN + f"{4 * ' '}Votre choix: ")

            if choix_enquete == "1":
                # Créer une nouvelle enquête
                nom = input(Fore.GREEN + f"{8 * ' '}Nom de l'enquête: ")
                date_de_debut = input(
                    Fore.GREEN + f"{8 * ' '}Date de début (YYYY-MM-DD): "
                )
                date_de_fin = input(Fore.GREEN + f"{8 * ' '}Date de fin (YYYY-MM-DD): ")
                try:
                    nouvelle_enquete = creer_enquete(nom, date_de_debut, date_de_fin)
                    print(Fore.BLUE + f"{8 * ' '}Enquête créée: {nouvelle_enquete}")
                except ValueError as e:
                    print(Fore.RED + f"{8 * ' '}Erreur: {e}")

            elif choix_enquete == "2":
                # Modifier une enquête
                enquetes = afficher_enquete()
                enquete_choisie = choisir_enquete(enquetes)
                if enquete_choisie:
                    afficher_menu_enquete(enquete_choisie)

            elif choix_enquete == "3":
                # Supprimer une enquête
                supprimer_enquete()

            elif choix_enquete == "4":
                # Retour au menu principal
                continue

            else:
                print(Fore.RED + "Choix invalide.")

        elif choix == "2":
            print(Fore.CYAN + "\nConsultation des Données:")
            print(Fore.YELLOW + "1. Afficher les personnes")
            print(Fore.YELLOW + "2. Afficher les preuves")
            print(Fore.YELLOW + "3. Afficher les événements")
            print(Fore.YELLOW + "4. Retour au menu principal")

            choix_donnees = input(Fore.GREEN + f"{4 * ' '}Votre choix: ")

            if choix_donnees == "1":
                # Afficher les personnes
                for i in pers_brut:
                    print(Fore.BLUE + f"{i["nom"]} {i["prenom"]}")

            elif choix_donnees == "2":
                # Afficher les preuves
                for i in preuve_brut:
                    print(Fore.BLUE + f"{i['nom']} : {i['type']}")

            elif choix_donnees == "3":
                # Afficher les événements
                for i in evenement_brut:
                    print(Fore.BLUE + f"{i['nom']}")

            elif choix_donnees == "4":
                # Retour au menu principal
                continue

            else:
                print(Fore.RED + "Choix invalide.")

        elif choix == "3":
            # Lancer l'interface graphique
            GUI.PoliceManagementApp().run()
            sortie = True

        elif choix == "4":
            # Quitter
            sortie = True

        else:
            print(Fore.RED + "Choix invalide. Veuillez réessayer.")

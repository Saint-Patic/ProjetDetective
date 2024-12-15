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
from commandes_terminale import *

if __name__ == "__main__":
    vide = " "
    sortie = False
    nom_dossier = "fichiers/"
    evenement_brut = charger_donnees(f"{nom_dossier}evenement.json")
    interro_brut = charger_donnees(f"{nom_dossier}interrogatoires.json")
    enquete_brut = charger_donnees(f"{nom_dossier}enquetes.json")
    pers_brut = charger_donnees(f"{nom_dossier}personnes.json")
    preuve_brut = charger_donnees(f"{nom_dossier}preuves.json")

    while not sortie:
        print("\nMenu:")
        print(f"{4 * vide}1. Créer une nouvelle enquête")
        print(f"{4 * vide}2. Choisir une enquête")
        print(f"{4 * vide}3. Afficher les enquêtes existantes")
        print(f"{4 * vide}4. Quitter")
        choix = input(f"{4 * vide}Votre choix: ")

        if choix == "1":
            nom = input(f"{8 * vide}Nom de l'enquête: ")
            date_de_debut = input(f"{8 * vide}Date de début (YYYY-MM-DD): ")
            date_de_fin = input(
                f"{8 * vide}Date de fin (YYYY-MM-DD) (9999-12-31 si enquete non finie): "
            )
            try:
                nouvelle_enquete = creer_enquete(nom, date_de_debut, date_de_fin)
                print(f"{8 * vide}Enquête créée: {nouvelle_enquete}")
            except ValueError as e:
                print(f"{8 * vide}Erreur: {e}")

        elif choix == "2":
            enquetes = afficher_enquete()
            enquete_choisie = choisir_enquete(enquetes)

            if enquete_choisie:
                ajout = True
                while ajout:
                    print(f"{12 * vide}1. Ajouter une personne")
                    print(f"{12 * vide}2. Lier une enquête")
                    print(f"{12 * vide}3. Ajouter un évènement")
                    print(f"{12 * vide}4. Ajouter une preuve")
                    print(f"{12 * vide}5. Retour au menu")
                    choix_ajout = input(f"{12 * vide}Votre choix: ")

                    if choix_ajout == "1":
                        taille_pers_brut = len(pers_brut)
                        for i in range(taille_pers_brut):
                            print(
                                f"{16 * vide}{i + 1}. {pers_brut[i]['nom']} {pers_brut[i]['prenom']}"
                            )
                        print(
                            f"{16 * vide}{taille_pers_brut + 1}. Créer une nouvelle personne"
                        )

                        try:
                            choix_personne = int(
                                input(
                                    f"{16 * vide}Votre choix (1 - {taille_pers_brut + 1}): "
                                )
                            )

                            if 1 <= choix_personne <= taille_pers_brut:
                                personne_ajoutee = pers_brut[choix_personne - 1]
                                personne_ajoutee = modifier_personne(personne_ajoutee)
                            elif choix_personne == taille_pers_brut + 1:
                                personne_ajoutee = creer_personne()
                            else:
                                raise ValueError("Choix invalide.")

                            enquete_choisie.ajouter_personne(personne_ajoutee)
                            print(f"{16 * vide}Personne ajoutée avec succès.")

                        except (ValueError, IndexError) as e:
                            print(f"{16 * vide}Erreur: {e}")

                    elif choix_ajout == "2":
                        taille_enquete_brut = len(enquete_brut)
                        for i in range(taille_enquete_brut):
                            print(f"{16 * vide}{i + 1}. {enquete_brut[i]['nom']}")

                        try:
                            choix_enquete = int(
                                input(
                                    f"{16 * vide}Votre choix (1 - {taille_enquete_brut}): "
                                )
                            )
                            if 1 <= choix_enquete <= taille_enquete_brut:
                                enquete_a_lier = dict_vers_enquete(
                                    enquete_brut[choix_enquete - 1]
                                )
                                enquete_choisie.ajouter_enquetes_liees(enquete_a_lier)
                                print(f"{16 * vide}Enquête liée avec succès.")
                            else:
                                raise ValueError("Choix invalide.")

                        except (ValueError, IndexError) as e:
                            print(f"{16 * vide}Erreur: {e}")

                    elif choix_ajout == "3":
                        enquete_choisie.afficher_evenements()
                    elif choix_ajout == "4":
                        enquete_choisie.afficher_preuves()
                    elif choix_ajout == "5":
                        ajout = False

                    enquete_choisie.sauvegarder_enquete()

        elif choix == "3":
            GUI.PoliceManagementApp().run()
            break

        elif choix == "4":
            break

        rep = input("    Quitter (oui/non) ? ").lower()
        sortie = rep == "oui"

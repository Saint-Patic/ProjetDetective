from colorama import Fore, init
import GUI
from utilitaire.commandes_terminale import *

init(autoreset=True)


def afficher_menu():
    print(Fore.CYAN + "\nMenu:")
    print(Fore.YELLOW + f"{4 * ' '}1. Créer une nouvelle enquête")
    print(Fore.YELLOW + f"{4 * ' '}2. Choisir une enquête")
    print(Fore.YELLOW + f"{4 * ' '}3. Afficher les enquêtes existantes")
    print(Fore.YELLOW + f"{4 * ' '}4. Quitter")


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
        afficher_menu()
        choix = input(Fore.GREEN + f"{4 * ' '}Votre choix: ")

        if choix == "1":
            nom = input(Fore.GREEN + f"{8 * ' '}Nom de l'enquête: ")
            date_de_debut = input(Fore.GREEN + f"{8 * ' '}Date de début (YYYY-MM-DD): ")
            date_de_fin = input(
                Fore.GREEN
                + f"{8 * ' '}Date de fin (YYYY-MM-DD) (9999-12-31 si enquête non finie): "
            )
            try:
                nouvelle_enquete = creer_enquete(nom, date_de_debut, date_de_fin)
                print(Fore.BLUE + f"{8 * ' '}Enquête créée: {nouvelle_enquete}")
            except ValueError as e:
                print(Fore.RED + f"{8 * ' '}Erreur: {e}")

        elif choix == "2":
            enquetes = afficher_enquete()
            enquete_choisie = choisir_enquete(enquetes)

            if enquete_choisie:
                ajout = True
                while ajout:
                    print(Fore.CYAN + f"{12 * ' '}Menu Enquête:")
                    print(Fore.YELLOW + f"{12 * ' '}1. Ajouter une personne")
                    print(Fore.YELLOW + f"{12 * ' '}2. Lier une enquête")
                    print(Fore.YELLOW + f"{12 * ' '}3. Créer un événement")
                    print(Fore.YELLOW + f"{12 * ' '}4. Ajouter une preuve")
                    print(Fore.YELLOW + f"{12 * ' '}5. Retour au menu principal")
                    choix_ajout = input(Fore.GREEN + f"{12 * ' '}Votre choix: ")

                    if choix_ajout == "1":
                        taille_pers_brut = len(pers_brut)
                        for i in range(taille_pers_brut):
                            print(
                                Fore.BLUE
                                + f"{16 * ' '}{i + 1}. {pers_brut[i]['nom']} {pers_brut[i]['prenom']}"
                            )
                        print(
                            Fore.YELLOW
                            + f"{16 * ' '}{taille_pers_brut + 1}. Créer une nouvelle personne"
                        )

                        try:
                            choix_personne = int(
                                input(
                                    Fore.GREEN
                                    + f"{16 * ' '}Votre choix (1 - {taille_pers_brut + 1}): "
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
                            print(
                                Fore.BLUE + f"{16 * ' '}Personne ajoutée avec succès."
                            )

                        except (ValueError, IndexError) as e:
                            print(Fore.RED + f"{16 * ' '}Erreur: {e}")

                    elif choix_ajout == "2":
                        taille_enquete_brut = len(enquete_brut)
                        for i in range(taille_enquete_brut):
                            print(
                                Fore.BLUE
                                + f"{16 * ' '}{i + 1}. {enquete_brut[i]['nom']}"
                            )

                        try:
                            choix_enquete = int(
                                input(
                                    Fore.GREEN
                                    + f"{16 * ' '}Votre choix (1 - {taille_enquete_brut}): "
                                )
                            )
                            if 1 <= choix_enquete <= taille_enquete_brut:
                                enquete_a_lier = dict_vers_enquete(
                                    enquete_brut[choix_enquete - 1]
                                )
                                enquete_choisie.ajouter_enquetes_liees(enquete_a_lier)
                                print(
                                    Fore.BLUE + f"{16 * ' '}Enquête liée avec succès."
                                )
                            else:
                                raise ValueError("Choix invalide.")

                        except (ValueError, IndexError) as e:
                            print(Fore.RED + f"{16 * ' '}Erreur: {e}")

                    elif choix_ajout == "3":
                        evenement_a_lier = creer_evenement(enquete_choisie)
                        enquete_choisie.ajouter_evenement(evenement_a_lier)
                        print(Fore.BLUE + f"{16 * ' '}Événement ajouté avec succès.")

                    elif choix_ajout == "4":
                        preuve_a_lier = creer_preuve(enquete_choisie)
                        enquete_choisie.ajouter_preuves(preuve_a_lier)
                        print(Fore.BLUE + f"{16 * ' '}Preuve ajoutée avec succès.")
                    elif choix_ajout == "5":
                        ajout = False

                    enquete_choisie.sauvegarder_enquete()

        elif choix == "3":
            GUI.PoliceManagementApp().run()
            sortie = True

        elif choix == "4":
            sortie = True

        else:
            print(Fore.RED + "Choix invalide. Veuillez réessayer.")

        if not sortie:
            rep = input(Fore.GREEN + "    Quitter (oui/non) ? ").lower()
            sortie = rep == "oui"

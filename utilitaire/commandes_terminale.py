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
import uuid
from colorama import Fore


def charger_donnees(chemin_fichier):
    """Charge les données JSON depuis un fichier."""
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def organiser_par_section(donnees, chemin_preuves=None):
    """Organise les personnes et preuves par sections."""
    sections = {
        "Employes": [],
        "Criminels": [],
        "Suspects": [],
        "Témoins": [],
        "Preuves": [],
    }
    for personne in donnees:
        classe = personne.get("classe", "Inconnu")
        if classe in ["Employe", "Suspect", "Criminel"]:
            sections[classe + "s"].append(personne)
    if chemin_preuves:
        sections["Preuves"].extend(charger_donnees(chemin_preuves))
    return sections

def creer_personne():
    """
    Fonction pour créer une instance d'une classe dérivée de `Personne` (Temoin, Suspect, Criminel ou Employe).
    Demande à l'utilisateur de choisir un type, de fournir les informations nécessaires, et d'ajouter des informations supplémentaires.
    """
    types_personne = {
        "temoin": Temoin,
        "suspect": Suspect,
        "criminel": Criminel,
        "employe": Employe,
    }

    # Demander le type de personne
    choix = input(
        "Quel type de personne voulez-vous créer ? (temoin, suspect, criminel, employe): "
    ).lower()

    if choix not in types_personne:
        print("Type de personne invalide.")
        return None

    # Collecter les informations de base
    nom = input("Entrez le nom : ")
    prenom = input("Entrez le prénom : ")
    date_de_naissance = input("Entrez la date de naissance (YYYY-MM-DD) : ")
    sexe = (
        input("Entrez le sexe (optionnel, appuyez sur Entrée pour ignorer) : ")
        or "pas de sexe précisé"
    )

    # Créer l'instance correspondante
    kwargs = {}
    if choix == "criminel":
        niveau_de_dangerosite = int(input("Entrez le niveau de dangerosité (1-5) : "))
        kwargs["niveau_de_dangerosite"] = niveau_de_dangerosite
    elif choix == "employe":
        grade = (
            input(
                "Entrez le grade (ex: gardien de la paix, appuyez sur Entrée pour garder la valeur par défaut) : "
            )
            or "gardien de la paix"
        )
        division = (
            input("Entrez la division (optionnel, appuyez sur Entrée pour ignorer) : ")
            or "pas de division"
        )
        kwargs["grade"] = grade
        kwargs["division"] = division

    classe_personne = types_personne[choix]
    personne = classe_personne(nom, prenom, date_de_naissance, sexe, **kwargs)

    # Demander d'ajouter des informations supplémentaires
    ajouter_infos = input(
        "Voulez-vous rajouter des informations supplémentaires ? (oui/non) : "
    ).lower()
    while ajouter_infos == "oui":
        if choix == "temoin":
            commentaire = input("Entrez un commentaire pour le témoignage : ")
            date_reception = input(
                "Entrez la date de réception du témoignage (YYYY-MM-DD) : "
            )
            personne.ajout_temoinage(commentaire, date_reception)
        elif choix == "suspect":
            alibi = input(
                "Entrez l'alibi (optionnel, appuyez sur Entrée pour ignorer) : "
            )
            suspection = input(
                "Entrez la suspection (optionnel, appuyez sur Entrée pour ignorer) : "
            )
            if alibi:
                personne.alibi = alibi
            if suspection:
                personne.suspection = suspection
        elif choix == "criminel":
            categorie_apparence = input(
                "Entrez une catégorie pour l'apparence (ex: tatouage, vêtements) : "
            )
            description_apparence = input(
                "Entrez la description pour cette apparence : "
            )
            personne.ajouter_apparence(categorie_apparence, description_apparence)
        elif choix == "employe":
            mail = input(
                "Entrez l'adresse mail de l'employé (optionnel, appuyez sur Entrée pour ignorer) : "
            )
            if mail:
                personne.mail = mail

        ajouter_infos = input(
            "Voulez-vous rajouter d'autres informations ? (oui/non) : "
        ).lower()

    return personne


def modifier_personne(personne):
    """
    Fonction pour modifier les données d'une instance de `Personne` ou ses classes dérivées.
    Permet de mettre à jour les attributs existants et d'ajouter des informations spécifiques à chaque type.

    Args:
        personne (Personne): L'instance de Personne à modifier.
    """
    if not type(personne) == dict:
        print("L'objet fourni n'est pas un dictionnaire")
        return
    if (
        input(
            f"Modifier les données de : {personne['nom']} {personne['prenom']} (oui/non) ? "
        )
        .strip()
        .lower()
        == "oui"
    ):
        print(f"Modification des données pour : {personne}")
        continuer = True

        while continuer:
            print("\nListe des attributs modifiables :")
            for attribut, valeur in personne.items():
                print(f"- {attribut} : {valeur}")

            choix = (
                input(
                    "\nEntrez le nom de l'attribut à modifier ou 'ajouter' pour des informations supplémentaires : "
                )
                .strip()
                .lower()
            )

            if choix in personne:
                nouvelle_valeur = input(f"Entrez la nouvelle valeur pour '{choix}' : ")
                # Convertir au bon type si nécessaire
                valeur_actuelle = personne[choix]
                try:
                    if isinstance(valeur_actuelle, int):
                        nouvelle_valeur = int(nouvelle_valeur)
                    elif isinstance(valeur_actuelle, float):
                        nouvelle_valeur = float(nouvelle_valeur)
                except ValueError:
                    print("Type invalide. L'attribut sera traité comme une chaîne.")
                personne[choix] = nouvelle_valeur
            elif choix == "ajouter":
                # Ajouter des informations spécifiques en fonction du type de l'instance
                if isinstance(personne, Temoin):
                    commentaire = input("Entrez un commentaire pour le témoignage : ")
                    date_reception = input(
                        "Entrez la date de réception (YYYY-MM-DD) : "
                    )
                    personne.ajout_temoinage(commentaire, date_reception)
                    print("Témoignage ajouté avec succès.")
                elif isinstance(personne, Suspect):
                    alibi = input("Entrez un nouvel alibi (optionnel) : ")
                    suspection = input("Entrez une nouvelle suspection (optionnel) : ")
                    if alibi:
                        personne.alibi = alibi
                    if suspection:
                        personne.suspection = suspection
                    print("Informations du suspect mises à jour avec succès.")
                elif isinstance(personne, Criminel):
                    categorie = input(
                        "Entrez une catégorie (ex: tatouage, vêtements, etc.) : "
                    )
                    description = input("Entrez la description : ")
                    personne.ajouter_apparence(categorie, description)
                    print("Description d'apparence ajoutée avec succès.")
                elif isinstance(personne, Employe):
                    mail = input("Entrez un nouvel e-mail (optionnel) : ")
                    if mail:
                        personne.mail = mail
                    print("Informations de l'employé mises à jour avec succès.")
            else:
                print("Attribut non reconnu ou action non valide.")

            continuer = (
                input("Voulez-vous continuer à modifier cette personne ? (oui/non) : ")
                .strip()
                .lower()
                == "oui"
            )
    # Transformer le dictionnaire en objet de la classe correspondante
    classe_mapping = {
        "Temoin": Temoin,
        "Suspect": Suspect,
        "Criminel": Criminel,
        "Employe": Employe,
    }
    classe_courante = personne["classe"]
    if classe_courante in classe_mapping:
        classe = classe_mapping[classe_courante]
        try:
            personne = classe(
                **personne
            )  # Crée une instance en passant le dictionnaire comme arguments

        except TypeError as e:
            print(f"Erreur lors de la transformation : {e}")
            return
    else:
        print("Classe inconnue. Aucune modification n'a été effectuée.")
        return

    return personne


def creer_enquete(nom, date_de_debut, date_de_fin):
    """Crée une nouvelle enquête et la sauvegarde dans enquetes.json."""
    try:
        utils.convertir_date(date_de_debut)
        utils.convertir_date(date_de_fin)
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYY-MM-DD.")

    if date_de_debut > date_de_fin:
        raise ValueError("La date de début doit être inférieure à la date de fin.")
    if date_de_debut < utils.convertir_date(datetime.datetime.now()):
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
        num_enquete = int(input("        Choisir un numéro d'enquête: "))
        if num_enquete < 1 or num_enquete > len(enquetes):
            print(f"Numéro invalide.")
            return None
        # Convertir l'enquête en une instance de la classe Enquete
        enquete_choisie = enquetes[num_enquete - 1]

        return dict_vers_enquete(enquete_choisie)

    except ValueError:
        print(f"Veuillez entrer un numéro valide.")
        return None


def dict_vers_enquete(dict_enquete):
    """Convertit un dictionnaire en une instance de la classe Enquete."""
    enquete = Enquete(
        nom=dict_enquete["nom"],
        date_de_debut=utils.convertir_date(dict_enquete["date_de_debut"]),
        date_de_fin=utils.convertir_date(
            dict_enquete.get("date_de_fin", "Enquête non clôturée")
        ),
        liste_preuves=dict_enquete.get("liste_preuves", []),
        personne_impliquee=dict_enquete.get("personne_impliquee", []),
    )

    # Affecter directement les autres attributs (en cas de sauvegarde/rechargement)
    enquete.id = dict_enquete.get("id", str(uuid.uuid4()))
    enquete.liste_evenement = dict_enquete.get("liste_evenement", [])
    enquete.enquetes_liees = dict_enquete.get("enquetes_liees", [])
    enquete.id_preuve = dict_enquete.get("id_preuve", 0)
    enquete.id_evenement = dict_enquete.get("id_evenement", 0)

    return enquete


def dict_vers_evenement(dict_evenement):
    """Convertit un dictionnaire en une instance de la classe Evenement."""
    evenement = Evenement(
        id=dict_evenement["id"],
        nom=dict_evenement["nom"],
        enquete_liee=dict_evenement["enquete_liee"],
        date_evenement=utils.convertir_date(
            dict_evenement.get("date_evenement", datetime.date.today())
        ),
        lieu=dict_evenement.get("lieu", "Lieu pas précisé"),
    )

    return evenement


def creer_evenement(enquete_liee):
    """Crée un nouvel événement et sauvegarde dans evenements.json."""
    new_id = str(uuid.uuid4())
    nom = input("        Entrez le nom de l'événement : ")
    id_enquete = enquete_liee.id
    date_evenement = input("Entrez le date_evenement (YYYY-MM-DD) : ")
    lieu = input("Entrez le lieu : ")

    try:
        utils.convertir_date(date_evenement)
    except ValueError:
        raise ValueError("La date doit être au format YYYY-MM-DD.")

    return Evenement(new_id, nom, id_enquete, date_evenement, lieu)


def creer_preuve(enquete_liee):
    """Crée une nouvelle preuve et sauvegarde dans preuves.json."""
    new_id = str(uuid.uuid4())
    nom = input("        Entrez le nom de la preuve : ")
    type_preuve = input("Entrez le type de preuve (ex: photo, document, etc.) : ")
    id_enquete = enquete_liee.id
    lieu_preuve = input("Entrez le lieu où la preuve a été trouvée : ")

    return Preuve(new_id, nom, id_enquete, type_preuve, lieu_preuve)


def supprimer_enquete():
    """Supprime une enquête du fichier enquetes.json."""
    nom_dossier = "fichiers/"
    fichier_enquetes = f"{nom_dossier}enquetes.json"

    try:
        # Charger les enquêtes existantes
        with open(fichier_enquetes, "r", encoding="utf-8") as fichier:
            enquetes = json.load(fichier)

        if not enquetes:
            print(Fore.YELLOW + "Aucune enquête à supprimer.")
            return

        # Afficher les enquêtes disponibles
        print(Fore.CYAN + "\nEnquêtes disponibles :")
        for index, enquete in enumerate(enquetes, start=1):
            print(f"{index}. {enquete['nom']} (Début: {enquete['date_de_debut']})")

        # Demander à l'utilisateur de choisir une enquête
        choix = int(input(Fore.GREEN + f"\nVotre choix (1 - {len(enquetes)}): "))
        if 1 <= choix <= len(enquetes):
            enquete_supprimee = enquetes.pop(choix - 1)

            # Sauvegarder les modifications
            with open(fichier_enquetes, "w", encoding="utf-8") as fichier:
                json.dump(enquetes, fichier, indent=4, ensure_ascii=False)

            print(
                Fore.BLUE
                + f"L'enquête '{enquete_supprimee['nom']}' a été supprimée avec succès."
            )
        else:
            print(Fore.RED + "Choix invalide.")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(Fore.RED + f"Erreur lors de la suppression : {e}")


def afficher_menu():
    print(Fore.CYAN + "\nMenu:")
    print(Fore.YELLOW + f"{4 * ' '}1. Créer une nouvelle enquête")
    print(Fore.YELLOW + f"{4 * ' '}2. Choisir une enquête")
    print(Fore.YELLOW + f"{4 * ' '}3. Afficher les enquêtes existantes")
    print(Fore.YELLOW + f"{4 * ' '}4. Supprimer une enquête")
    print(Fore.YELLOW + f"{4 * ' '}5. Quitter")


def afficher_menu_enquete(enquete_choisie):
    nom_dossier = "fichiers/"
    enquete_brut = charger_donnees(f"{nom_dossier}enquetes.json")
    pers_brut = charger_donnees(f"{nom_dossier}personnes.json")
    ajout = True
    while ajout:
        print(Fore.CYAN + f"{12 * ' '}Menu Enquête: ")
        print(Fore.YELLOW + f"{12 * ' '}1. Ajouter une personne")
        print(Fore.YELLOW + f"{12 * ' '}2. Lier une enquête")
        print(Fore.YELLOW + f"{12 * ' '}3. Supprimer une enquête liée")
        print(Fore.YELLOW + f"{12 * ' '}4. Créer un événement")
        print(Fore.YELLOW + f"{12 * ' '}5. Ajouter une preuve")
        print(Fore.YELLOW + f"{12 * ' '}6. Modifier l'enquête")
        print(Fore.YELLOW + f"{12 * ' '}7. Retour au menu principal")

        choix_ajout = input(Fore.GREEN + f"{12 * ' '}Votre choix: ")

        if choix_ajout == "1":
            # Ajouter une personne
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
                print(Fore.BLUE + f"{16 * ' '}Personne ajoutée avec succès.")

            except (ValueError, IndexError) as e:
                print(Fore.RED + f"{16 * ' '}Erreur: {e}")

        elif choix_ajout == "2":
            # Lier une enquête
            taille_enquete_brut = len(enquete_brut)
            for i in range(taille_enquete_brut):
                print(Fore.BLUE + f"{16 * ' '}{i + 1}. {enquete_brut[i]['nom']}")

            try:
                choix_enquete = int(
                    input(
                        Fore.GREEN
                        + f"{16 * ' '}Votre choix (1 - {taille_enquete_brut}): "
                    )
                )
                if 1 <= choix_enquete <= taille_enquete_brut:
                    enquete_a_lier = dict_vers_enquete(enquete_brut[choix_enquete - 1])
                    enquete_choisie.ajouter_enquetes_liees(enquete_a_lier)
                    print(Fore.BLUE + f"{16 * ' '}Enquête liée avec succès.")
                else:
                    raise ValueError("Choix invalide.")

            except (ValueError, IndexError) as e:
                print(Fore.RED + f"{16 * ' '}Erreur: {e}")

        elif choix_ajout == "3":
            # Supprimer une enquête liée
            if not enquete_choisie.enquetes_liees:
                print(Fore.RED + f"{16 * ' '}Aucune enquête liée à supprimer.")
            else:
                for i, enquete in enumerate(enquete_choisie.enquetes_liees, 1):
                    print(
                        Fore.BLUE
                        + f"{16 * ' '}{i}. {enquete['nom']} (ID: {enquete['id']})"
                    )

                try:
                    choix_suppression = int(
                        input(
                            Fore.GREEN
                            + f"{16 * ' '}Choisissez une enquête à supprimer (1 - {len(enquete_choisie.enquetes_liees)}): "
                        )
                    )

                    if 1 <= choix_suppression <= len(enquete_choisie.enquetes_liees):
                        enquete_id = enquete_choisie.enquetes_liees[
                            choix_suppression - 1
                        ]["id"]
                        enquete_choisie.supprimer_enquete_liee(enquete_id)
                        print(
                            Fore.BLUE + f"{16 * ' '}Enquête liée supprimée avec succès."
                        )
                    else:
                        raise ValueError("Choix invalide.")

                except (ValueError, IndexError) as e:
                    print(Fore.RED + f"{16 * ' '}Erreur: {e}")

        elif choix_ajout == "4":
            # Créer un événement
            evenement_a_lier = creer_evenement(enquete_choisie)
            enquete_choisie.ajouter_evenement(evenement_a_lier)
            print(Fore.BLUE + f"{16 * ' '}Événement ajouté avec succès.")

        elif choix_ajout == "5":
            # Ajouter une preuve
            preuve_a_lier = creer_preuve(enquete_choisie)
            enquete_choisie.ajouter_preuves(preuve_a_lier)
            print(Fore.BLUE + f"{16 * ' '}Preuve ajoutée avec succès.")

        elif choix_ajout == "6":
            # Modifier l'enquête
            print(
                Fore.GREEN
                + f"{16 * ' '}Modification de l'enquête '{enquete_choisie.nom}'"
            )
            nom = input(
                Fore.GREEN
                + f"{8 * ' '}Nom de l'enquête (actuel: {enquete_choisie.nom}): "
            )
            date_de_debut = input(
                Fore.GREEN
                + f"{8 * ' '}Date de début (actuelle: {enquete_choisie.date_de_debut}): "
            )
            date_de_fin = input(
                Fore.GREEN
                + f"{8 * ' '}Date de fin (actuelle: {enquete_choisie.date_de_fin}): "
            )

            try:
                enquete_choisie.nom = nom
                enquete_choisie.date_de_debut = date_de_debut
                enquete_choisie.date_de_fin = date_de_fin
                print(Fore.BLUE + f"{16 * ' '}Enquête modifiée avec succès.")
            except ValueError as e:
                print(Fore.RED + f"{16 * ' '}Erreur: {e}")

        elif choix_ajout == "7":
            # Retour au menu principal
            ajout = False

        enquete_choisie.sauvegarder_enquete()


def chargement_donnees():
    nom_dossier = "fichiers/"
    enquete_brut = charger_donnees(f"{nom_dossier}enquetes.json")
    pers_brut = charger_donnees(f"{nom_dossier}personnes.json")
    preuve_brut = charger_donnees(f"{nom_dossier}preuves.json")
    evenement_brut = charger_donnees(f"{nom_dossier}evenement.json")
    interro_brut = charger_donnees(f"{nom_dossier}interrogatoires.json")
    return evenement_brut, interro_brut, enquete_brut, pers_brut, preuve_brut

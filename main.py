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
    if not isinstance(personne, Personne):
        print(
            "L'objet fourni n'est pas une instance de Personne ou de ses classes dérivées."
        )
        return

    print(f"Modification des données pour : {personne}")
    continuer = True

    while continuer:
        print("\nListe des attributs modifiables :")
        for attribut, valeur in vars(personne).items():
            print(f"- {attribut} : {valeur}")

        choix = (
            input(
                "\nEntrez le nom de l'attribut à modifier ou 'ajouter' pour des informations supplémentaires : "
            )
            .strip()
            .lower()
        )

        if choix in vars(personne):
            nouvelle_valeur = input(f"Entrez la nouvelle valeur pour '{choix}' : ")
            # Convertir au bon type si nécessaire
            valeur_actuelle = getattr(personne, choix)
            try:
                if isinstance(valeur_actuelle, int):
                    nouvelle_valeur = int(nouvelle_valeur)
                elif isinstance(valeur_actuelle, float):
                    nouvelle_valeur = float(nouvelle_valeur)
            except ValueError:
                print("Type invalide. L'attribut sera traité comme une chaîne.")
            setattr(personne, choix, nouvelle_valeur)
            print(f"L'attribut '{choix}' a été modifié avec succès.")
        elif choix == "ajouter":
            # Ajouter des informations spécifiques en fonction du type de l'instance
            if isinstance(personne, Temoin):
                commentaire = input("Entrez un commentaire pour le témoignage : ")
                date_reception = input("Entrez la date de réception (YYYY-MM-DD) : ")
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
    vide = " "
    with open("fichiers/enquetes.json", "r", encoding="utf-8") as f:
        enquetes = json.load(f)
        for idx, enquete in enumerate(enquetes, 1):
            print(
                f"{8*vide}{idx}. {enquete['nom']} ({enquete['date_de_debut']} - {enquete['date_de_fin']})"
            )
    return enquetes


def choisir_enquete(enquetes):
    """Permet de choisir une enquête parmi celles listées."""

    try:
        num_enquete = int(input("        Choisir un numéro d'enquête: "))
        if num_enquete < 1 or num_enquete > len(enquetes):
            print(f"{8*vide}Numéro invalide.")
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
        print(f"{8*vide}Veuillez entrer un numéro valide.")
        return None


if __name__ == "__main__":
    vide = " "
    sortie = False
    ajout = True
    nom_dossier = "fichiers/"
    evenement_brut = charger_donnees(f"{nom_dossier}evenement.json")
    interro_brut = charger_donnees(f"{nom_dossier}interrogatoires.json")
    enquete_brut = charger_donnees(f"{nom_dossier}enquetes.json")
    pers_brut = charger_donnees(f"{nom_dossier}personnes.json")
    preuve_brut = charger_donnees(f"{nom_dossier}preuves.json")
    while not sortie:
        # menu de base
        print("\nMenu:")
        print(f"{4*vide}1. Créer une nouvelle enquête")
        print(f"{4*vide}2. Choisir une enquête")
        print(f"{4*vide}3. Afficher les enquêtes existantes")
        print(f"{4*vide}4. Quitter")
        choix = input(f"{4*vide}Votre choix: ")
        if choix == "1":  # nouvelle enquete
            nom = input(f"{8*vide}Nom de l'enquête: ")
            date_de_debut = input(f"{8*vide}Date de début (YYYY-MM-DD): ")
            date_de_fin = input(f"{8*vide}Date de fin (YYYY-MM-DD): ")
            nouvelle_enquete = creer_enquete(nom, date_de_debut, date_de_fin)
            print(f"{8*vide}Enquête créée: {nouvelle_enquete}")
        elif choix == "2":  # choisir une enquete pour ajouter des donnees
            enquetes = afficher_enquete()  # affiche le choix d'enquete à modifier
            enquete_choisie = choisir_enquete(enquetes)
            if enquete_choisie:
                while (
                    ajout
                ):  # boucle pour ne pas devoir repasser par le menu de base à chaque fois
                    print(f"{12*vide}1. Ajouter une personne")
                    print(f"{12*vide}2. Lier une enquête")
                    print(f"{12*vide}3. Ajouter un évènement")
                    print(f"{12*vide}4. Ajouter une preuve")
                    print(f"{12*vide}5. Retour au menu")
                    choix_ajout = input(f"{12*vide}votre choix: ")
                    if choix_ajout == "1":  # ajout personne
                        taille_pers_brut = len(pers_brut)
                        for i in range(
                            taille_pers_brut
                        ):  # affiche toutes les personnes dispos
                            print(
                                f"{16*vide}{i + 1}. {pers_brut[i]['nom']} {pers_brut[i]['prenom']}"
                            )
                        print(
                            f"{16*vide}{taille_pers_brut + 1}. Créer une nouvelle personne"
                        )
                        choix_personne = int(
                            input(
                                f"{16*vide}Ajouter une personne déjà dans la base de données (1 - {taille_pers_brut}) ou en ajouter une nouvelle {taille_pers_brut + 1} : "
                            )
                        )
                        if (
                            choix_personne < taille_pers_brut + 1
                        ):  # si personne déjà dans la base de données
                            personne_ajoute = pers_brut[choix_personne - 1]
                            if (
                                input(
                                    f"Modifier les données de : {personne_ajoute["nom"]} {personne_ajoute["prenom"]} (oui/non) ? "
                                )
                                == "oui"
                            ):
                                modifier_personne(personne_ajoute)
                        else:
                            personne_ajoute = creer_personne()
                        enquete_choisie.ajouter_personne(personne_ajoute)
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

        rep = input("    Quitter (oui/non) ? ")
        sortie = True if rep == "oui" else False

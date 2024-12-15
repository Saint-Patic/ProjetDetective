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
    id = str(uuid.uuid4())
    nom = input("        Entrez le nom de l'événement : ")
    id_enquete = enquete_liee.id
    date_evenement = input("Entrez le date_evenement (YYYY-MM-DD) : ")
    lieu = input("Entrez le lieu : ")

    try:
        utils.convertir_date(date_evenement)
    except ValueError:
        raise ValueError("La date doit être au format YYYY-MM-DD.")

    return Evenement(id, nom, id_enquete, date_evenement, lieu)


def creer_preuve(enquete_liee):
    """Crée une nouvelle preuve et sauvegarde dans preuves.json."""
    id = str(uuid.uuid4())
    nom = input("        Entrez le nom de la preuve : ")
    type_preuve = input("Entrez le type de preuve (ex: photo, document, etc.) : ")
    id_enquete = enquete_liee.id
    lieu_preuve = input("Entrez le lieu où la preuve a été trouvée : ")

    return Preuve(id, nom, id_enquete, type_preuve, lieu_preuve)

from utilitaire import utils
import json
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


def creer_enquete(nom, date_de_debut, date_de_fin):
    """Crée une nouvelle enquête et la sauvegarde dans enquetes.json."""
    try:
        utils.convertir_date(date_de_debut)
        utils.convertir_date(date_de_fin)
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYY-MM-DD.")

    nouvelle_enquete = Enquete(nom, date_de_debut, date_de_fin)
    return nouvelle_enquete


def afficher_enquete():
    with open("fichiers/enquetes.json", "r", encoding="utf-8") as f:
        enquetes = json.load(f)
        for enquete in enquetes:
            print(
                f"{enquete['nom']} ({enquete['date_de_debut']} - {enquete['date_de_fin']})"
            )


if __name__ == "__main__":
    sortie = False
    while not sortie:
        print("\nMenu:")
        print("1. Créer une nouvelle enquête")
        print("2. Choisir une enquete")
        print("3. Afficher les enquêtes existantes")
        print("4. Quitter")
        choix = input("Votre choix: ")
        if choix == "1":
            nom = input("Nom de l'enquête: ")
            date_de_debut = input("Date de début (YYYY-MM-DD): ")
            date_de_fin = input("Date de fin (YYYY-MM-DD): ")
            nouvelle_enquete = creer_enquete(nom, date_de_debut, date_de_fin)
            print(f"Enquête créée: {nouvelle_enquete}")
        elif choix == "2":
            afficher_enquete()
        elif choix == "3":
            pass
        elif choix == "4":
            sortie = True

        rep = input("Quitter (oui/non) ?")
        sortie = True if rep == "oui" else False

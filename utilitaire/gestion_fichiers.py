import json
from classes import Personne, Temoin, Suspect, Employe, Criminel


def lecture_json(fichier):
    try:
        with open(fichier, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Le fichier JSON '{fichier}' n'a pas été trouvé \n")
        return None
    except FileExistsError:
        print(f"Le fichier JSON existe '{fichier}' déjà \n")
        return None
    except json.JSONDecodeError:
        print("Le fichier JSON est mal formaté \n")
        return None
    except Exception as e:
        print(f"Erreur inconnue: {e}\n")
        return None


def create_person(personne: dict):
    class_map = {
        "Personne": Personne,
        "Temoin": Temoin,
        "Suspect": Suspect,
        "Employe": Employe,
        "Criminel": Criminel,
    }
    classe_name = personne.get("classe", "Personne")  # Valeur par défaut "Personne"
    classe_trouvee = class_map.get(classe_name, Personne)

    # Récupérer les attributs de base
    nom = personne["nom"]
    prenom = personne["prenom"]
    date_de_naissance = personne["date_de_naissance"]
    sexe = personne.get("sexe", "'pas de sexe précisé'")

    # Filtrer les attributs supplémentaires à passer comme kwargs
    kwargs = {
        k: v
        for k, v in personne.items()
        if k not in ["nom", "prenom", "date_de_naissance", "sexe", "classe"]
    }

    return classe_trouvee(
        nom=nom, prenom=prenom, date_de_naissance=date_de_naissance, sexe=sexe, **kwargs
    )


def liste_personne(fichier):
    data = lecture_json(fichier)
    if data:
        return [create_person(personne) for personne in data]
    else:
        return None


if __name__ == "__main__":
    # Test avec un fichier JSON existant
    people = liste_personne(r"fichiers\personnes.json")
    for person in people:
        print(person)

    # test avec un fichier JSON non existant
    people = liste_personne(r"fichiers\personnes_non_existant.json")

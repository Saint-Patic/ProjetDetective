import json
from classes import Person, Temoin, Suspect, Employe, Criminel


def lecture_json(fichier):
    try:
        # Ouverture du fichier JSON
        with open(fichier, "r") as file:
            # Lecture des données JSON
            data = json.load(file)

        return data

    except FileNotFoundError:
        print("Le fichier JSON n'a pas été trouvé: \n")
        return None
    except FileExistsError:
        print("Le fichier JSON existe déjà: \n")
        return None
    except json.JSONDecodeError:
        print("Le fichier JSON est mal formaté: \n")
        return None
    except Exception as e:
        print(f"Erreur inconnue: {e}\n")
        return None


def create_person(data):
    class_map = {
        "Person": Person,
        "Temoin": Temoin,
        "Suspect": Suspect,
        "Employe": Employe,
        "Criminel": Criminel,
    }
    classe_name = data.get(
        "classe", "Person"
    )  # Default to "Person" if "classe" is not specified
    classe = class_map.get(classe_name, Person)
    return classe(
        nom=data["nom"],
        prenom=data["prenom"],
        date_de_naissance=data["date_de_naissance"],
        sexe=data.get("sexe", "'pas de sexe précisé'"),
    )


if __name__ == "__main__":
    # Test avec un fichier JSON existant
    data = lecture_json("fichiers\personnes.json")
    people = [create_person(person) for person in data]
    for person in people:
        print(person)

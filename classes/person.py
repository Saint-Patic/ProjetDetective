import uuid  # Import pour générer un identifiant unique
from datetime import datetime
import json


class Personne:

    def __init__(
        self,
        nom: str,
        prenom: str,
        date_de_naissance: str,
        sexe="'pas de sexe précisé'",
        **kwargs,
    ):
        """
        Pré : nom (str), prenom (str), date_de_naissance (str) au format "YYYY-MM-DD", sexe (str) (optionnel), kwargs (dict) (optionnel)
        Post : Crée un objet Personne avec les attributs spécifiés
        """
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self._date_de_naissance = datetime.strptime(date_de_naissance, "%Y-%m-%d")
        self._date_de_deces = datetime.strptime("9999-12-31", "%Y-%m-%d")
        self.metier = "'Pas de métier actuellement'"
        self.interrogatoires = {}
        self.mail = ""
        for cle, valeur in kwargs.items():
            setattr(self, cle, valeur)

    @property
    def date_de_naissance(self):
        """
        Pré : -
        Post : Retourne la date de naissance au format "YYYY-MM-DD"
        """
        return self._date_de_naissance.strftime("%Y-%m-%d")

    @date_de_naissance.setter
    def date_de_naissance(self, valeur: str) -> None:
        """
        Pré : valeur (str) au format "YYYY-MM-DD"
        Post : Définit la date de naissance, lève une exception si la date est dans le futur
        """
        try:
            date_obj = datetime.strptime(valeur, "%Y-%m-%d")
            if date_obj > datetime.now():
                raise ValueError(
                    "La date de naissance ne peut pas être dans le futur.\n"
                )
            self._date_de_naissance = date_obj
        except ValueError as e:
            print(f"Erreur lors de la définition de la date de naissance: {e}\n")

    @property
    def date_de_deces(self):
        """
        Pré : -
        Post : Retourne la date de décès au format "YYYY-MM-DD"
        """
        return self._date_de_deces.strftime("%Y-%m-%d")

    @date_de_deces.setter
    def date_de_deces(self, valeur: str) -> None:
        """
        Pré : valeur (str) au format "YYYY-MM-DD"
        Post : Définit la date de décès, lève une exception si la date est dans le futur ou avant la date de naissance
        Raise ValueError: si la date de décès est dans le futur ou avant la date de naissance
        """
        try:
            date_obj = datetime.strptime(valeur, "%Y-%m-%d")
            if date_obj > datetime.now():
                raise ValueError("La date de décès ne peut pas être dans le futur.\n")
            if date_obj < self._date_de_naissance:
                raise ValueError(
                    "La date de décès doit être supérieure à la date de naissance.\n"
                )
            self._date_de_deces = date_obj
        except ValueError as e:
            print(f"Erreur lors de la définition de la date de décès: {e}\n")

    def ajouter_interrogatoire(self, date: str, enqueteur, num_enquete: int) -> None:
        """
        Ajoute un interrogatoire à la liste des interrogatoires et le sauvegarde dans un fichier JSON sans doublons.
        """
        try:
            date_modifiee = datetime.strptime(date, "%Y-%m-%d")
            if (
                enqueteur._date_de_naissance > date_modifiee
                or self._date_de_naissance > date_modifiee
            ):
                raise ValueError("L'enquêteur ou l'interrogé n'est pas encore né.\n")
            if (
                enqueteur._date_de_deces < date_modifiee
                or self._date_de_deces < date_modifiee
            ):
                raise ValueError(
                    "L'enquêteur ou l'interrogé est mort. Il ne peut pas participer à l'interrogatoire.\n"
                )

            # Génération de l'ID unique
            interrogatoire_id = str(uuid.uuid4())

            # Nouvel interrogatoire
            nouvel_interrogatoire = {
                "id": interrogatoire_id,
                "date": date,
                "enqueteur": enqueteur.prenom,
                "interroge": self.prenom,
                "num_enquete": num_enquete,
            }

            # Sauvegarde dans le fichier JSON
            try:
                with open(
                    "fichiers/interrogatoires.json", "r", encoding="utf-8"
                ) as fichier:
                    donnees_existantes = json.load(fichier)
            except (FileNotFoundError, json.JSONDecodeError):
                donnees_existantes = []

            # Vérification des doublons
            for interrogatoire in donnees_existantes:
                if (
                    interrogatoire.get("date") == nouvel_interrogatoire["date"]
                    and interrogatoire.get("enqueteur")
                    == nouvel_interrogatoire["enqueteur"]
                    and interrogatoire.get("interroge")
                    == nouvel_interrogatoire["interroge"]
                    and interrogatoire.get("num_enquete")
                    == nouvel_interrogatoire["num_enquete"]
                ):
                    print("Cet interrogatoire existe déjà. Ajout ignoré.\n")
                    return  # Ne rien ajouter si l'interrogatoire existe déjà

            # Ajouter le nouvel interrogatoire si aucun doublon trouvé
            donnees_existantes.append(nouvel_interrogatoire)

            with open(
                "fichiers/interrogatoires.json", "w", encoding="utf-8"
            ) as fichier:
                json.dump(donnees_existantes, fichier, indent=4, ensure_ascii=False)

            # Ajout local à l'objet
            interrogatoires_date = self.interrogatoires.get(date, [])
            interrogatoires_date.append(
                {
                    "id": interrogatoire_id,
                    "enqueteur": enqueteur.prenom,
                    "num_enquete": num_enquete,
                }
            )
            self.interrogatoires[date] = interrogatoires_date

        except ValueError as e:
            print(f"Erreur lors de l'ajout de l'interrogatoire: {e}\n")

    def obtenir_interrogatoires(self, date: str) -> list:
        """
        Pré : date (str) au format "YYYY-MM-DD"
        Post : Retourne la liste des interrogatoires pour une date donnée, lève une exception si la date est invalide ou si aucun interrogatoire n'est trouvé
        Raise KeyError : si aucun interrogatoire trouvé pour la date donnée
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            if date not in self.interrogatoires:
                raise KeyError(f"Aucun interrogatoire trouvé pour la date : {date}\n")
            return self.interrogatoires[date]
        except (ValueError, KeyError) as e:
            print(f"Erreur lors de la récupération des interrogatoires: {e}\n")
            return []

    def to_dict(self) -> dict:
        """
        Pré : -
        Post : Retourne un dictionnaire contenant les informations de l'objet Personne
        """
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_de_naissance": self.date_de_naissance,
            "date_de_deces": self.date_de_deces,
            "sexe": self.sexe,
            "metier": self.metier,
            "interrogatoires": self.interrogatoires,
            "mail": self.mail,
        }

    def __str__(self) -> str:
        """
        Pré : -
        Post : Retourne une chaîne décrivant la personne avec son nom, prénom, date de naissance et métier
        """
        return f"{self.nom} {self.prenom}, né le {self.date_de_naissance}, travaille comme {self.metier}"


if __name__ == "__main__":
    pass

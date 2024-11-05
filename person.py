from datetime import datetime


class Person:
    def __init__(
        self, nom, prenom, sexe="pas de sexe précisé", date_de_naissance="9999-12-31"
    ):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.date_de_deces = datetime.strptime("9999-12-31", "%Y-%m-%d")
        self.lieu_de_naissance = ""
        self.metier = "Pas de métier actuellement"
        self.interrogatoires = []
        self.mail = ""
        self._date_de_naissance = datetime.strptime(date_de_naissance, "%Y-%m-%d")

    @property
    def date_de_naissance(self):
        return self._date_de_naissance.strftime("%Y-%m-%d")

    @date_de_naissance.setter
    def date_de_naissance(self, value):
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Le format de la date doit être AAAA-MM-JJ.")

        if date_obj > datetime.now():
            raise ValueError("La date de naissance ne peut pas être dans le futur.")

        self._date_de_naissance = date_obj

    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}, né le {self.date_de_naissance}, travaille comme {self.metier}"

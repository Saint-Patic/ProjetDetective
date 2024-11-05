from datetime import datetime


class Person:

    def __init__(
        self,
        nom: str,
        prenom: str,
        date_de_naissance: str,
        sexe="pas de sexe précisé",
    ):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self._date_de_naissance = datetime.strptime(date_de_naissance, "%Y-%m-%d")
        self._date_de_deces = datetime.strptime("9999-12-31", "%Y-%m-%d")
        self.lieu_de_naissance = ""
        self.metier = "Pas de métier actuellement"
        self.interrogatoires = {}
        self.mail = ""

    @property
    def date_de_naissance(self):
        return self._date_de_naissance.strftime("%Y-%m-%d")

    @date_de_naissance.setter
    def date_de_naissance(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Le format de la date doit être AAAA-MM-JJ.")

        if date_obj > datetime.now():
            raise ValueError("La date de naissance ne peut pas être dans le futur.")

        self._date_de_naissance = date_obj

    @property
    def date_de_deces(self):
        return self.date_de_deces.strftime("%Y-%m-%d")

    @date_de_deces.setter
    def date_de_deces(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Le format de la date doit être AAAA-MM-JJ.")

        if date_obj > datetime.now():
            raise ValueError("La date de décès ne peut pas être dans le futur.")

        if date_obj < self.date_de_naissance:
            raise ValueError(
                "La date de décès doit être supérieure à la date de naissance."
            )

        self.date_de_deces = date_obj

    def add_interrogatoire(self, date: str, enqueteur: str, num_enquete: int):
        interrogatoires_date = self.interrogatoires.get(date, [])
        interrogatoires_date.append(
            {"enqueteur": enqueteur, "num_enquete": num_enquete}
        )
        self.interrogatoires[date] = interrogatoires_date

    def get_interrogatoires(self, date: str) -> list:

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Le format de la date doit être AAAA-MM-JJ.")

        if date not in self.interrogatoires:
            raise KeyError(f"Aucun interrogatoire trouvé pour la date : {date}")

        return self.interrogatoires[date]

    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}, né le {self.date_de_naissance}, travaille comme {self.metier}"


class Suspect(Person):
    def __init__(
        self, nom, prenom, sexe="pas de sexe précisé", date_de_naissance="9999-12-31"
    ):
        super().__init__(nom, prenom, sexe, date_de_naissance)
        self.innocent = False
        self.statut_legal = False
        self.suspection = ""
        self.alibi = ""


class Temoin(Person):
    def __init__(
        self, nom, prenom, sexe="pas de sexe précisé", date_de_naissance="9999-12-31"
    ):
        super().__init__(nom, prenom, sexe, date_de_naissance)


class Criminel(Person):
    def __init__(self):
        super().__init__()


class Employee(Person):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":

    enqueteur1 = Person("Demarcq", "Alexis", "2003-08-04")

    Nathan = Person("Lemaire", "Nathan", "2003-07-30")
    Nathan.sexe = "homme"
    Nathan.metier = "chômeur"
    Nathan.add_interrogatoire("2004-07-30", enqueteur1, 1)
    Nathan.add_interrogatoire("2004-07-31", enqueteur1, 2)
    Nathan.add_interrogatoire("2004-07-31", enqueteur1, 3)
    print(Nathan.interrogatoires)
    print(Nathan.get_interrogatoires("2004-07-30"))
    print(Nathan)

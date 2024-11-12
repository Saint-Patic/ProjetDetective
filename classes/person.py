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
            if date_obj > datetime.now():
                raise ValueError(
                    "La date de naissance ne peut pas être dans le futur.\n"
                )
            self._date_de_naissance = date_obj
        except ValueError as e:
            print(f"Erreur lors de la définition de la date de naissance: {e}\n")

    @property
    def date_de_deces(self):
        return self._date_de_deces.strftime("%Y-%m-%d")

    @date_de_deces.setter
    def date_de_deces(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            if date_obj > datetime.now():
                raise ValueError("La date de décès ne peut pas être dans le futur.\n")
            if date_obj < self._date_de_naissance:
                raise ValueError(
                    "La date de décès doit être supérieure à la date de naissance.\n"
                )
            self._date_de_deces = date_obj
        except ValueError as e:
            print(f"Erreur lors de la définition de la date de décès: {e}\n")

    def add_interrogatoire(self, date: str, enqueteur, num_enquete: int) -> None:
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
            interrogatoires_date = self.interrogatoires.get(date, [])
            interrogatoires_date.append(
                {"enqueteur": enqueteur.prenom, "num_enquete": num_enquete}
            )
            self.interrogatoires[date] = interrogatoires_date
        except ValueError as e:
            print(f"Erreur lors de l'ajout de l'interrogatoire: {e}\n")

    def get_interrogatoires(self, date: str) -> list:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            if date not in self.interrogatoires:
                raise KeyError(f"Aucun interrogatoire trouvé pour la date : {date}\n")
            return self.interrogatoires[date]
        except (ValueError, KeyError) as e:
            print(f"Erreur lors de la récupération des interrogatoires: {e}\n")
            return []

    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}, né le {self.date_de_naissance}, travaille comme {self.metier}"


if __name__ == "__main__":
    pass

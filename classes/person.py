from datetime import datetime


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
        return self._date_de_deces.strftime("%Y-%m-%d")

    @date_de_deces.setter
    def date_de_deces(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            if date_obj > datetime.now():
                print("Erreur : La date de décès ne peut pas être dans le futur.")
            elif date_obj < self._date_de_naissance:
                print(
                    "Erreur : La date de décès doit être supérieure à la date de naissance."
                )
            else:
                self._date_de_deces = date_obj
        except ValueError:
            print("Erreur : Le format de la date doit être AAAA-MM-JJ.")


if __name__ == "__main__":

    pass

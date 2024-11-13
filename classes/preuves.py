from datetime import date, datetime


class Preuve:

    def __init__(
        self,
        id: int,
        nom: str,
        enquete_liee: int,
        type=" Type non spécifié",
        lieu="Lieu non spécifié",
        date_preuve=date.today(),
        heure="Heure non spécifée",
    ):
        self.id = id
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.type = type
        self.lieu = lieu
        self.date_preuve = date_preuve
        self.heure = heure

    def __str__(self) -> str:
        return (f"ID: {self.id}, Nom: {self.nom}, Enquete liée: {self.enquete_liee}, Type: {self.type},"
                f" Lieu: {self.lieu}, "f" Date: {self.date_preuve}, Heure: {self.heure}")


if __name__ == "__main__":
    pass
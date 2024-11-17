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
        """
        Pré : id (int), nom (str), enquete_liee (int), type (str) (optionel), lieu (str) (optionel) ,
        date_de_naissance (str) au format "YYYY-MM-DD", heure (str) (optionnelle)
        Post : Crée une instance de la classe Preuve avec les attributs spécifiés
        """
        self.id = id
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.type = type
        self.lieu = lieu
        self.date_preuve = date_preuve
        self.heure = heure

    def ajouter_type(self, type):
        """
        Pré : type(str)
        Post : Definit l'attribut type de la preuve
        """
        self.type = type

    def ajouter_lieu(self, lieu):
        """
        Pré : lieu (str)
        Post : Définit l'attribut lieu de la preuve
        """
        self.lieu = lieu

    def ajouter_date(self, nouvelle_date):
        """
        Pré : date au format YYYY-MM-DD
        Post : Définit la date ou la preuve à été trouvée
        """
        self.date_event = nouvelle_date

    def ajouter_heure(self, heure):
        """
        Pré : date au format YYYY-MM-DD
        Post : Définit l'heure ou la preuve à été trouvée
        """
        self.heure = heure


    def __str__(self) -> str:
        """
        Pré : -
        Post : return une string contenant les attributs
        """
        return (f"ID: {self.id}, Nom: {self.nom}, Enquete liée: {self.enquete_liee}, Type: {self.type},"
                f" Lieu: {self.lieu}, "f" Date: {self.date_preuve}, Heure: {self.heure}")


if __name__ == "__main__":
    pass
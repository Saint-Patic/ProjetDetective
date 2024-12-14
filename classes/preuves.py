from datetime import date, datetime
from utilitaire import utils


class Preuve:

    def __init__(
        self,
        id: int,
        nom: str,
        enquete_liee: int,
        type=" Type non spécifié",
        lieu="Lieu non spécifié",
        date_preuve=utils.convertir_date(datetime.today()),
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
        Post : Définit la date de quand la preuve a été trouvée
        """
        self.date_preuve = nouvelle_date

    def ajouter_heure(self, heure):
        """
        Pré : date au format YYYY-MM-DD
        Post : Définit l'heure à laquelle la preuve a été trouvée
        """
        self.heure = heure

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "enquete_liee": self.enquete_liee,
            "type": self.type,
            "lieu": self.lieu,
            "date_preuve": self.date_preuve,
            "heure": self.heure,
        }

    def __str__(self) -> str:
        """
        Pré : -
        Post : return une string contenant les attributs
        """
        return (
            f"ID: {self.id}, Nom: {self.nom}, Enquete liée: {self.enquete_liee}, Type: {self.type},"
            f" Lieu: {self.lieu}, "
            f" Date: {self.date_preuve}, Heure: {self.heure}"
        )


if __name__ == "__main__":
    pass

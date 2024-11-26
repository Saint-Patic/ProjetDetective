from datetime import date


class Evenement:

    def __init__(
        self,
        id: int,
        nom: str,
        enquete_liee: int,
        date_event=date.today(),
        lieu="Lieu pas précisé",
    ):
        """
        Pré : id (int), nom (str), enquete_liee (int), lieu (str) (optionel) ,
        date_de_naissance (str) au format "YYYY-MM-DD"
        Post : Crée une instance de la classe Evenement avec les attributs spécifiés
        """
        self.id = id
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.date_event = date_event
        self.lieu = lieu

    def ajouter_date(self, nouvelle_date):
        """
        Pré : date au format YYYY-MM-DD
        Post : Définit la date ou l'évenement s'est passé
        """
        self.date_event = nouvelle_date

    def ajouter_lieu(self, lieu):
        """
        Pré : lieu (str)
        Post : Définit l'attribut lieu de l'évenement
        """
        self.lieu = lieu

    def to_dict(self) -> dict:
        """
        Pré : -
        Post : Retourne un dictionnaire contenant les informations de l'objet Evenement
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "enquete_liee": self.enquete_liee,
            "date_event": (
                self.date_event.strftime("%Y-%m-%d")
                if isinstance(self.date_event, date)
                else self.date_event
            ),
            "lieu": self.lieu,
        }

    def __str__(self) -> str:
        """
        Pré : -
        Post : return une string contenant les attributs
        """
        return (
            f"ID: {self.id}, Nom: {self.nom}, Enquete liée: {self.enquete_liee}, Date: {self.date_event},"
            f"Lieu: {self.lieu}"
        )


if __name__ == "__main__":
    pass

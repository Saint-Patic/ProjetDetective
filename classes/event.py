from datetime import date


class Evenement:

    def __init__(self, id: int, nom: str, enquete_liee : int , date_event=date.today(), lieu = "Lieu pas précisé"):
        self.id = id
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.date_event = date_event
        self.lieu = lieu

    def ajouter_date(self, nouvelle_date)->None:
        self.date_event = nouvelle_date

    def add_lieu(self, lieu) -> None:
        self.lieu = lieu

    def __str__(self) -> str:
        return (f"ID: {self.id}, Nom: {self.nom}, Enquete liée: {self.enquete_liee}, Date: {self.date_event},"
                f"Lieu: {self.lieu}")

if __name__ == "__main__":
    pass
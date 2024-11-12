from datetime import date


class Evenement:

    def __init__(self, nom: str, enquete_liee : int , date=date.today(), lieu = "Lieu pas précisé"):
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.date = date
        self.lieu = lieu

    def add_date(self, date)->None:
        self.date = date

    def add_lieu(self, lieu) -> None:
        self.lieu = lieu

    def __str__(self):
        return f"{self.nom} - {self.enquete_liee} - {self.date} - {self.lieu}"

if __name__ == "__main__":
   pass
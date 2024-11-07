from datetime import date


class Evenement:

    def __init__(self, nom: str, enquete_liee : int , date=date.today(), lieu = "Pas précisé"):
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.date = date
        self.lieu = lieu

    def add_date(self, date)->None:
        self.date = date

    def add_place(self, place) -> None:
        self.place = place

if __name__ == "__main__":
   pass
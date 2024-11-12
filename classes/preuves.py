from datetime import date, datetime
class Preuve:

    def __init__(self, id: int, nom : str, enquete_liee:int, type = "non spécifié", lieu = "non spécifié", date_preuve = date.today(), heure = "non spécifée"):
        self.id = id
        self.nom = nom
        self.enquete_liee = enquete_liee
        self.type = type
        self.lieu = lieu
        self.date_preuve = date_preuve
        self.heure = heure

    def __str__(self):
        return f"{self.id} - {self.nom}"

from .person import Person


class Temoin(Person):
    def __init__(
        self,
        nom,
        prenom,
        date_de_naissance,
        sexe="pas de sexe précisé",
    ):
        super().__init__(nom, prenom, date_de_naissance, sexe)
        self.temoignage = {}
        self.fiabilite = 0
        self.protectino = False
        self.disponibilite = False

    def add_temoinage(self, commentaire, date_de_reception):
        if date_de_reception not in self.temoignages:
            self.apparence[date_de_reception] = []
        self.apparence[date_de_reception].append(commentaire)

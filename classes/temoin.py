from .person import Personne


class Temoin(Personne):

    def __init__(
        self,
        nom,
        prenom,
        date_de_naissance,
        sexe="pas de sexe précisé",
        **kwargs,
    ):
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.temoignage = {}
        self.fiabilite = 0
        self.protectino = False
        self.disponibilite = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_temoinage(self, commentaire, date_de_reception):
        if date_de_reception not in self.temoignages:
            self.apparence[date_de_reception] = []
        self.apparence[date_de_reception].append(commentaire)

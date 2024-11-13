from .person import Personne


class Suspect(Personne):

    def __init__(
        self, nom, prenom, date_de_naissance, sexe="pas de sexe précisé", **kwargs
    ):
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.innocent = False
        self.statut_legal = False
        self.suspection = ""
        self.alibi = ""
        for key, value in kwargs.items():
            setattr(self, key, value)

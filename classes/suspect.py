from .person import Person


class Suspect(Person):

    def __init__(self, nom, prenom, date_de_naissance, sexe="pas de sexe précisé"):
        super().__init__(nom, prenom, date_de_naissance, sexe)
        self.innocent = False
        self.statut_legal = False
        self.suspection = ""
        self.alibi = ""

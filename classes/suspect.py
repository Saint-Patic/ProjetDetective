from person import Person


class Suspect(Person):
    def __init__(
        self, nom, prenom, sexe="pas de sexe précisé", date_de_naissance="9999-12-31"
    ):
        super().__init__(nom, prenom, sexe, date_de_naissance)
        self.innocent = False
        self.statut_legal = False
        self.suspection = ""
        self.alibi = ""
from .person import Personne


class Suspect(Personne):

    def __init__(
        self, nom, prenom, date_de_naissance, sexe="pas de sexe précisé", **kwargs
    ):
        """
        Pré : nom (str), prenom (str), date_de_naissance (str) au format "YYYY-MM-DD", sexe (str) (optionnel), kwargs (dict) (optionnel)
        Post : Crée une instance de la classe Suspect avec les attributs spécifiés
        """
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.innocent = False
        self.statut_legal = False
        self.suspection = ""
        self.alibi = ""
        for key, value in kwargs.items():
            setattr(self, key, value)

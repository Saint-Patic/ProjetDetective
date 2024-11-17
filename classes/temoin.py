from .person import Personne


class Temoin(Personne):

    def __init__(
        self,
        nom: str,
        prenom: str,
        date_de_naissance: str,
        sexe: str = "pas de sexe précisé",
        **kwargs,
    ):
        """
        Pré : nom (str), prenom (str), date_de_naissance (str) au format "YYYY-MM-DD", sexe (str) (optionnel), kwargs (dict) (optionnel)
        Post : Crée une instance de la classe Temoin avec les attributs spécifiés
        """
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.temoignage = {}
        self.fiabilite = 0
        self.protection = False
        self.disponibilite = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_temoinage(self, commentaire, date_de_reception):
        """
        Pré : commentaire (str), date_de_reception (str) au format "YYYY-MM-DD"
        Post : Ajoute un témoignage à la liste des témoignages du témoin
        """
        if date_de_reception not in self.temoignage:
            self.temoignage[date_de_reception] = []
        self.temoignage[date_de_reception].append(commentaire)

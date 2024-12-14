from .person import Personne


class Criminel(Personne):

    def __init__(
        self,
        nom: str,
        prenom: str,
        date_de_naissance: str,
        sexe: str = "pas de sexe précisé",
        niveau_de_dangerosite: int = 1,
        **kwargs,
    ):
        """
        Pré : nom (str), prenom (str), date_de_naissance (str) au format "YYYY-MM-DD", sexe (str) (optionnel), niveau_de_dangerosite (int) (optionnel), kwargs (dict) (optionnel)
        Post : Crée une instance de la classe Criminel avec les attributs spécifiés
        """
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.niveau_de_dangerosite = niveau_de_dangerosite
        self.apparence = {}
        self.corpulence = {}
        self.dossier_psychologique = {}
        self.lieu_de_detention = ""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def ajouter_apparence(self, categorie: str, description: str):
        """
        Pré : categorie (str), description (str)
        Post : Ajoute une description d'apparence à la liste des apparences du criminel
        """
        if categorie not in self.apparence:
            self.apparence[categorie] = []
        self.apparence[categorie].append(description)

    def ajouter_corpulence(self, categorie: str, description: str):
        """
        Pré : categorie (str), description (str)
        Post : Ajoute une description de corpulence à la liste des corpulences du criminel
        """
        self.corpulence[categorie] = description

    def ajouter_psychologie(self, categorie: str, observation: str):
        """
        Pré : categorie (str), observation (str)
        Post : Ajoute une observation psychologique à la liste des observations du criminel
        """
        if categorie not in self.dossier_psychologique:
            self.dossier_psychologique[categorie] = []
        self.dossier_psychologique[categorie].append(observation)

    def __str__(self) -> str:
        """
        Pré : Aucun
        Post : Retourne une représentation sous forme de chaîne de caractères de l'objet Criminel,
               incluant les informations personnelles, le niveau de dangerosité et le dossier psychologique
        """
        dossier_psy = "\n".join(
            f"{categorie}: {', '.join(observations)}"
            for categorie, observations in self.dossier_psychologique.items()
        )
        return f"{self.prenom} {self.nom}, {self.sexe}, {self.date_de_naissance}, lvl dangereux : {self.niveau_de_dangerosite}, Dossier Psychologique:\n{dossier_psy}"


if __name__ == "__main__":
    enqueteur1 = Personne("Demarcq", "Alexis", "2003-08-04")
    criminel1 = Criminel("Dupont", "Jean", "2003-07-30", "homme")

    criminel1.ajouter_apparence("Taille", "Petite")
    criminel1.ajouter_apparence("Taille", "1m60")

    criminel1.ajouter_corpulence("Poids", "Sous poids")
    criminel1.ajouter_corpulence("Poids", "50kg")

    print(f"{criminel1.apparence = }")
    print(f"{criminel1.corpulence = }")
    print(criminel1)

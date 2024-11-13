from .person import Personne


class Criminel(Personne):

    def __init__(
        self,
        nom,
        prenom,
        date_de_naissance,
        sexe="pas de sexe précisé",
        niveau_de_dangerosite=1,
        **kwargs,
    ):
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.niveau_de_dangerosite = niveau_de_dangerosite
        self.apparence = {}
        self.corpulence = {}
        self.dossier_psychologique = {}
        self.lieu_de_detention = ""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_apparence(self, categorie: str, description: str):
        if categorie not in self.apparence:
            self.apparence[categorie] = []
        self.apparence[categorie].append(description)

    def add_corpulence(self, categorie: str, description: str):
        self.corpulence[categorie] = description

    def add_psychologie(self, categorie: str, observation: str):
        if categorie not in self.dossier_psychologique:
            self.dossier_psychologique[categorie] = []
        self.dossier_psychologique[categorie].append(observation)

    def __str__(self) -> str:
        dossier_psy = "\n".join(
            f"{categorie}: {', '.join(observations)}"
            for categorie, observations in self.dossier_psychologique.items()
        )
        return f"{self.prenom} {self.nom}, {self.sexe}, {self.date_de_naissance}, lvl dangereux : {self.niveau_de_dangerosite}, Dossier Psychologique:\n{dossier_psy}"


if __name__ == "__main__":
    enqueteur1 = Personne("Demarcq", "Alexis", "2003-08-04")
    criminel1 = Criminel("Dupont", "Jean", "2003-07-30", "homme")

    criminel1.add_apparence("Taille", "Petite")
    criminel1.add_apparence("Taille", "1m60")

    criminel1.add_corpulence("Poids", "Sous poids")
    criminel1.add_corpulence("Poids", "50kg")

    print(f"{criminel1.apparence = }")
    print(f"{criminel1.corpulence = }")
    print(criminel1)

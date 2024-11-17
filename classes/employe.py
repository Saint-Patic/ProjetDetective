from .person import Personne


class Employe(Personne):
    _matricule_counter = 1

    def __init__(
        self,
        nom: str,
        prenom: str,
        date_de_naissance: str,
        sexe: str = "pas de sexe précisé",
        grade: str = "gardien de la paix",
        division: str = "pas de division",
        **kwargs,
    ):
        """
        Pré : nom (str), prenom (str), date_de_naissance (str) au format "YYYY-MM-DD", sexe (str) (optionnel), grade (str) (optionnel), division (str) (optionnel), kwargs (dict) (optionnel)
        Post : Crée une instance de la classe Employe avec les attributs spécifiés
        """
        super().__init__(nom, prenom, date_de_naissance, sexe, **kwargs)
        self.grade = grade
        self.division = division
        self.matricule = Employe._matricule_counter
        Employe._matricule_counter += 1
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        """
        Pré : Aucun
        Post : Retourne une représentation sous forme de chaîne de caractères de l'objet Employe,
               incluant le nom, prénom, matricule, grade, division et date de naissance.
        """
        return (
            f"{self.nom} {self.prenom}, Matricule: {self.matricule}, Grade: {self.grade}, "
            f"Division: {self.division}, Date de naissance: {self.date_de_naissance}"
        )

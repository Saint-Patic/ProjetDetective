from .person import Person


class Employe(Person):
    _matricule_counter = 1

    def __init__(
        self,
        nom,
        prenom,
        date_de_naissance,
        sexe="pas de sexe précisé",
        grade="gardien de la paix",
        division="pas de division",
    ):
        super().__init__(nom, prenom, date_de_naissance, sexe)
        self.grade = grade
        self.division = division
        self.matricule = Employe._matricule_counter
        Employe._matricule_counter += 1

    def __str__(self):
        return (
            f"{self.nom} {self.prenom}, Matricule: {self.matricule}, Grade: {self.grade}, "
            f"Division: {self.division}, Date de naissance: {self.date_de_naissance}"
        )
